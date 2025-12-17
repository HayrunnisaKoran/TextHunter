namespace TextHunter.Models
{
    public class PredictionResult
    {
        public string ModelName { get; set; } = string.Empty;
        public string Prediction { get; set; } = string.Empty;
        public Dictionary<string, double> Probabilities { get; set; } = new();
        public double HumanProbability { get; set; }
        public double AIProbability { get; set; }
    }
}

