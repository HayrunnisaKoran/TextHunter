namespace TextHunter.Models
{
    public class ComparisonViewModel
    {
        public string Text { get; set; } = string.Empty;
        public Dictionary<string, PredictionResult> Results { get; set; } = new();
    }
}

