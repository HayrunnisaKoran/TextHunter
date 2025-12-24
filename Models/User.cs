using System.ComponentModel.DataAnnotations;

namespace TextHunter.Models
{
    public class User
    {
        [Key]
        public int Id { get; set; }

        [Required, StringLength(100)]
        public string FullName { get; set; } = null!;

        [Required, EmailAddress]
        public string Email { get; set; } = null!;

        [Required]
        public string PasswordHash { get; set; } = null!; // Siber güvenlik için şifreyi açık metin tutmuyoruz

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        // Bir kullanıcının birden fazla analizi olabilir (İlişkisel veritabanı mantığı)
        public virtual ICollection<PredictionResultEntity> Predictions { get; set; } = new List<PredictionResultEntity>();
    }
}