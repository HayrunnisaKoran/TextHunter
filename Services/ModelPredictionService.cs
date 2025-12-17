using System.Diagnostics;
using System.Text.Json;
using TextHunter.Models;

namespace TextHunter.Services
{
    public class ModelPredictionService : IModelPredictionService
    {
        private readonly ILogger<ModelPredictionService> _logger;
        private readonly string _pythonScriptPath;
        private readonly string _pythonExecutable;

        public ModelPredictionService(ILogger<ModelPredictionService> logger, IConfiguration configuration)
        {
            _logger = logger;
            
            // Python script yolu
            var basePath = Directory.GetCurrentDirectory();
            _pythonScriptPath = Path.Combine(basePath, "Scripts", "predict.py");
            
            // Python executable yolu (varsayılan olarak python veya python3)
            _pythonExecutable = configuration["PythonExecutable"] ?? "python";
        }

        public async Task<PredictionResult> PredictAsync(string text, string modelName)
        {
            try
            {
                var results = await PredictMultipleModelsAsync(text);
                if (results.ContainsKey(modelName))
                {
                    return results[modelName];
                }
                
                return new PredictionResult
                {
                    ModelName = modelName,
                    Prediction = "Unknown",
                    HumanProbability = 0.0,
                    AIProbability = 0.0
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Tahmin yapılırken hata oluştu");
                throw;
            }
        }

        public async Task<Dictionary<string, PredictionResult>> PredictMultipleModelsAsync(string text)
        {
            var results = new Dictionary<string, PredictionResult>();

            try
            {
                // Python scriptini çalıştır
                var processStartInfo = new ProcessStartInfo
                {
                    FileName = _pythonExecutable,
                    Arguments = $"\"{_pythonScriptPath}\" \"{text.Replace("\"", "\\\"")}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processStartInfo);
                if (process == null)
                {
                    throw new Exception("Python process başlatılamadı");
                }

                var output = await process.StandardOutput.ReadToEndAsync();
                var error = await process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync();

                if (process.ExitCode != 0)
                {
                    _logger.LogError("Python script hatası: {Error}", error);
                    throw new Exception($"Python script hatası: {error}");
                }

                // JSON çıktısını parse et
                var jsonResult = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(output);
                
                if (jsonResult == null)
                {
                    throw new Exception("Python script çıktısı parse edilemedi");
                }

                // Her model için sonuçları işle
                foreach (var kvp in jsonResult)
                {
                    var modelName = kvp.Key;
                    var resultData = kvp.Value;

                    var predictionResult = new PredictionResult
                    {
                        ModelName = modelName
                    };

                    if (resultData.TryGetProperty("prediction", out var prediction))
                    {
                        predictionResult.Prediction = prediction.GetString() ?? "Unknown";
                    }

                    if (resultData.TryGetProperty("probabilities", out var probabilities))
                    {
                        var probDict = new Dictionary<string, double>();
                        foreach (var prob in probabilities.EnumerateObject())
                        {
                            probDict[prob.Name] = prob.Value.GetDouble();
                        }
                        predictionResult.Probabilities = probDict;

                        // Human ve AI olasılıklarını ayır
                        predictionResult.HumanProbability = probDict.ContainsKey("Human") 
                            ? probDict["Human"] 
                            : 0.0;
                        predictionResult.AIProbability = probDict.ContainsKey("AI") 
                            ? probDict["AI"] 
                            : 0.0;
                    }

                    results[modelName] = predictionResult;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Tahmin yapılırken hata oluştu");
                throw;
            }

            return results;
        }
    }
}

