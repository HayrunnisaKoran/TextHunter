using TextHunter.Models;

namespace TextHunter.Services
{
    public interface IModelPredictionService
    {
        Task<PredictionResult> PredictAsync(string text, string modelName);
        Task<Dictionary<string, PredictionResult>> PredictMultipleModelsAsync(string text);
    }
}

