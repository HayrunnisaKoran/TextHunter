using System.Diagnostics;
using System.Text.Json;
using TextHunter.Models;
using Microsoft.AspNetCore.Hosting;

namespace TextHunter.Services
{
    public class ModelPredictionService : IModelPredictionService
    {
        private readonly ILogger<ModelPredictionService> _logger;
        private readonly IWebHostEnvironment _env;
        private readonly string _pythonScriptPath;
        private readonly string _pythonExecutable;

        public ModelPredictionService(ILogger<ModelPredictionService> logger, IConfiguration configuration, IWebHostEnvironment env )
        {
            _logger = logger;
            _env = env;
            
            // Python script yolu
            
            _pythonScriptPath = Path.Combine(_env.ContentRootPath, "Scripts", "predict.py");
            
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

            try //bu kod blogu sankı cmd uzerınden python predict.py "metın" komutunu yazıyormusuz gıbı yapar 
            { 
                // Python scriptini çalıştır
                var processStartInfo = new ProcessStartInfo
                {
                    FileName = _pythonExecutable, //calıstırılacak python exe yolu
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
                var jsonResult = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(output); //test'e tabi
                
                if (jsonResult == null)
                {
                    throw new Exception("Python script çıktısı parse edilemedi");
                }

                // Her model için sonuçları işle
                foreach (var kvp in jsonResult)
                {
                    var resultData = kvp.Value;
                    var predictionResult = new PredictionResult { ModelName = kvp.Key };

                    if (resultData.TryGetProperty("prediction", out var pred))
                    {
                        string val = pred.ValueKind == JsonValueKind.Number ? pred.GetInt32().ToString() : pred.GetString();
                        // 0 gelirse Yapay Zeka, 1 gelirse İnsan diyoruz
                        predictionResult.Prediction = (val == "0" || val == "AI") ? "Yapay Zeka" : "İnsan";
                    }

                    if (resultData.TryGetProperty("probabilities", out var probabilities))
                    {
                        var probDict = new Dictionary<string, double>();
                        foreach (var prob in probabilities.EnumerateObject())
                        {
                            probDict[prob.Name] = prob.Value.GetDouble();
                        }
                        predictionResult.Probabilities = probDict;

                        // Python'dan gelen ham rakam anahtarlarını ("0" ve "1") kullanıyoruz
                        // Modeline göre: 0 = AI, 1 = Human
                        predictionResult.HumanProbability = probDict.ContainsKey("1") ? probDict["1"] : 0.0;
                        predictionResult.AIProbability = probDict.ContainsKey("0") ? probDict["0"] : 0.0;
                    }
                    results[kvp.Key] = predictionResult;
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

