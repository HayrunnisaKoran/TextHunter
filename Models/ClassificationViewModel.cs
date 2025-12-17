namespace TextHunter.Models
{
    public class ClassificationViewModel
    {
        public string Text { get; set; } = string.Empty;
        public string SelectedModel { get; set; } = "naive_bayes_bow";
        public PredictionResult? Result { get; set; }
        public List<string> AvailableModels { get; set; } = new();
    }
}

