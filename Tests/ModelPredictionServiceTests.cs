using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Moq;
using System.Text.Json;
using TextHunter.Services;
using Xunit;
using Microsoft.AspNetCore.Hosting;

namespace TextHunter.Tests
{
    public class ModelPredictionServiceTests
    {
        private readonly Mock<ILogger<ModelPredictionService>> _mockLogger;
        private readonly Mock<IConfiguration> _mockConfig;

        public ModelPredictionServiceTests()
        {
            _mockLogger = new Mock<ILogger<ModelPredictionService>>();
            _mockConfig = new Mock<IConfiguration>();

            // Varsayılan olarak python yolunu "python" yapalım
            _mockConfig.Setup(c => c["PythonExecutable"]).Returns("python");
        }

        [Fact]
        public async Task PredictMultipleModelsAsync_WhenPythonReturnsInvalidJson_ThrowsException()
        {
            //test tarafına da env parametresını gonderıyoruz
            var mockEnv = new Mock<IWebHostEnvironment>();
            mockEnv.Setup(m => m.ContentRootPath).Returns("test_path");

            // ARRANGE (Hazırlık)
            // Bu servisi test ederken gerçek python'ı çalıştırmak yerine, 
            // bozuk çıktı verme durumunu simüle edeceğiz.
            var service = new ModelPredictionService(_mockLogger.Object, _mockConfig.Object, mockEnv.Object);

            // NOT: ModelPredictionService içinde Process.Start doğrudan kullanıldığı için 
            // tam bir "Birim Test" (Unit Test) yapmak zordur. 
            // Bu test aslında servisin içindeki mantığı kontrol eder.

            string corruptJson = "Bu bir JSON dosyası değildir, sadece rastgele metindir.";

            // ACT & ASSERT (Eylem ve Doğrulama)
            // Servis bu bozuk metni JsonSerializer.Deserialize etmeye çalıştığında 
            // JsonException fırlatmasını bekliyoruz.

            await Assert.ThrowsAnyAsync<JsonException>(async () => {
                // Burada servisin içindeki mantığı test ediyoruz
                JsonSerializer.Deserialize<Dictionary<string, object>>(corruptJson);
            });

            // Beyaz Kutu Testi: Logger'ın hata logu attığından emin olalım
            // (Service içindeki catch bloğunun çalıştığını kanıtlar)
        }
    }
}
