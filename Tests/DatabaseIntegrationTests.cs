using Microsoft.EntityFrameworkCore;
using TextHunter.Data;
using TextHunter.Models;
using Xunit;

namespace TextHunter.Tests
{
    public class DatabaseIntegrationTests
    {
        private AppDbContext GetDatabaseContext()
        {
            // Her test için benzersiz bir veritabanı adı oluşturuyoruz
            var options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;

            var databaseContext = new AppDbContext(options);
            databaseContext.Database.EnsureCreated();
            return databaseContext;
        }

        [Fact]
        public async Task Can_Save_And_Retrieve_Prediction_Result()
        {
            // ARRANGE: Veritabanını ve kaydedilecek veriyi hazırla
            using var context = GetDatabaseContext();
            var testResult = new PredictionResultEntity 
            {
                InputText = "Bu analiz edilecek örnek bir metindir.",
                ModelName = "random_forest_tfidf",
                Prediction = "Human",
                AIProbability = 0.95,
                HumanProbability = 0.05,
                // Eğer veritabanında "AnalysisHistory" gibi bir tablo varsa onu kullanmalısın
            };

            // ACT: Veriyi kaydet
            context.PredictionResults.Add(testResult); //DbSet ısmıyle aynı
            await context.SaveChangesAsync();

            // ASSERT: Veriyi geri oku ve doğrula
            var savedResult = await context.PredictionResults.FirstOrDefaultAsync();

            Assert.NotNull(savedResult);
            Assert.Equal("Human", savedResult.Prediction);
        }
    }
}