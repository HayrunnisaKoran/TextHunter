using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace TextHunter.Models
{
    public class PredictionResultEntity
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string InputText { get; set; } = null!; // Analiz edilen metin

        public string Prediction { get; set; } = null!;// "İnsan" veya "AI" sonucu

        public double HumanProbability { get; set; } // US-5 yüzdelik oranları
        public double AIProbability { get; set; }

        public string ModelName { get; set; } = null!; // Naive Bayes, Random Forest veya SVM

        public DateTime AnalyzedAt { get; set; } = DateTime.UtcNow;

        // Foreign Key: Bu analiz hangi kullanıcıya ait? (Normalizasyon için şart)
        public int UserId { get; set; }

        [ForeignKey("UserId")]
        public User User { get; set; } = null!;
    }
}