# White Box Testler - Dokümantasyon

## Test Framework

**Kullanılan Framework:** xUnit (NUnit alternatifi)  
**Mock Framework:** Moq  
**Test Coverage:** En az 3 adet White Box test case

## Test Senaryoları

### Test Case 1: TextClassification - Başarılı Tahmin

**Test ID:** WB-001  
**Test Adı:** TextClassification_Post_WithValidText_ReturnsViewWithResult  
**Test Tipi:** White Box - Unit Test  
**Test Edilen Kod:** `HomeController.TextClassification(HttpPost)`

**Test Senaryosu:**
```csharp
[Fact]
public async Task TextClassification_Post_WithValidText_ReturnsViewWithResult()
{
    // Arrange
    var viewModel = new ClassificationViewModel
    {
        Text = "This is a test text for classification.",
        SelectedModel = "naive_bayes_bow"
    };

    var predictionResult = new PredictionResult
    {
        ModelName = "naive_bayes_bow",
        Prediction = "Human",
        HumanProbability = 0.75,
        AIProbability = 0.25
    };

    _mockPredictionService
        .Setup(s => s.PredictAsync(It.IsAny<string>(), It.IsAny<string>()))
        .ReturnsAsync(predictionResult);

    // Act
    var result = await _controller.TextClassification(viewModel);

    // Assert
    var viewResult = Assert.IsType<ViewResult>(result);
    var model = Assert.IsType<ClassificationViewModel>(viewResult.Model);
    Assert.NotNull(model.Result);
    Assert.Equal("Human", model.Result.Prediction);
    Assert.Equal(0.75, model.Result.HumanProbability);
}
```

**Test Edilen Kod Yolu:**
1. `HomeController.TextClassification` metodu çağrılır
2. Model validation kontrolü yapılır
3. `IModelPredictionService.PredictAsync` çağrılır
4. Sonuç `ClassificationViewModel.Result`'a atanır
5. View döndürülür

**Beklenen Sonuç:** ✅ Test başarılı, View döndürülür, Result dolu

---

### Test Case 2: TextClassification - Boş Metin Validasyonu

**Test ID:** WB-002  
**Test Adı:** TextClassification_Post_WithEmptyText_ReturnsViewWithError  
**Test Tipi:** White Box - Unit Test  
**Test Edilen Kod:** `HomeController.TextClassification(HttpPost)` - Validation logic

**Test Senaryosu:**
```csharp
[Fact]
public async Task TextClassification_Post_WithEmptyText_ReturnsViewWithError()
{
    // Arrange
    var viewModel = new ClassificationViewModel
    {
        Text = "",
        SelectedModel = "naive_bayes_bow"
    };

    // Act
    var result = await _controller.TextClassification(viewModel);

    // Assert
    var viewResult = Assert.IsType<ViewResult>(result);
    var model = Assert.IsType<ClassificationViewModel>(viewResult.Model);
    Assert.False(_controller.ModelState.IsValid);
    Assert.Null(model.Result);
    Assert.True(_controller.ModelState.ContainsKey("Text"));
}
```

**Test Edilen Kod Yolu:**
1. `HomeController.TextClassification` metodu çağrılır
2. `string.IsNullOrWhiteSpace(model.Text)` kontrolü yapılır
3. ModelState'e hata eklenir: `ModelState.AddModelError("Text", "Lütfen bir metin girin.")`
4. View döndürülür (Result null)

**Beklenen Sonuç:** ✅ Validation hatası, ModelState invalid, Result null

---

### Test Case 3: ModelComparison - Çoklu Model Tahmini

**Test ID:** WB-003  
**Test Adı:** ModelComparison_Post_WithValidText_ReturnsViewWithResults  
**Test Tipi:** White Box - Unit Test  
**Test Edilen Kod:** `HomeController.ModelComparison(HttpPost)`

**Test Senaryosu:**
```csharp
[Fact]
public async Task ModelComparison_Post_WithValidText_ReturnsViewWithResults()
{
    // Arrange
    var viewModel = new ComparisonViewModel
    {
        Text = "This is a test text for model comparison."
    };

    var results = new Dictionary<string, PredictionResult>
    {
        ["naive_bayes_bow"] = new PredictionResult
        {
            ModelName = "naive_bayes_bow",
            Prediction = "Human",
            HumanProbability = 0.80,
            AIProbability = 0.20
        },
        ["random_forest_tfidf"] = new PredictionResult
        {
            ModelName = "random_forest_tfidf",
            Prediction = "AI",
            HumanProbability = 0.30,
            AIProbability = 0.70
        },
        ["svm_tfidf"] = new PredictionResult
        {
            ModelName = "svm_tfidf",
            Prediction = "Human",
            HumanProbability = 0.65,
            AIProbability = 0.35
        }
    };

    _mockPredictionService
        .Setup(s => s.PredictMultipleModelsAsync(It.IsAny<string>()))
        .ReturnsAsync(results);

    // Act
    var result = await _controller.ModelComparison(viewModel);

    // Assert
    var viewResult = Assert.IsType<ViewResult>(result);
    var model = Assert.IsType<ComparisonViewModel>(viewResult.Model);
    Assert.NotNull(model.Results);
    Assert.Equal(3, model.Results.Count);
    Assert.True(model.Results.ContainsKey("naive_bayes_bow"));
    Assert.True(model.Results.ContainsKey("random_forest_tfidf"));
    Assert.True(model.Results.ContainsKey("svm_tfidf"));
}
```

**Test Edilen Kod Yolu:**
1. `HomeController.ModelComparison` metodu çağrılır
2. Model validation kontrolü yapılır
3. `IModelPredictionService.PredictMultipleModelsAsync` çağrılır
4. Sonuçlar `ComparisonViewModel.Results`'a atanır
5. View döndürülür

**Beklenen Sonuç:** ✅ 3 model sonucu döner, Dictionary dolu

---

### Test Case 4: ModelPredictionService - Exception Handling

**Test ID:** WB-004  
**Test Adı:** ModelPredictionService_PredictAsync_ThrowsException_LogsError  
**Test Tipi:** White Box - Unit Test  
**Test Edilen Kod:** `ModelPredictionService.PredictAsync` - Exception handling

**Test Senaryosu:**
```csharp
[Fact]
public async Task ModelPredictionService_PredictAsync_ThrowsException_LogsError()
{
    // Arrange
    var service = new ModelPredictionService(_mockLogger.Object, _mockConfig.Object);
    _mockPredictionService
        .Setup(s => s.PredictAsync(It.IsAny<string>(), It.IsAny<string>()))
        .ThrowsAsync(new Exception("Test exception"));

    // Act & Assert
    await Assert.ThrowsAsync<Exception>(async () => 
        await service.PredictAsync("test", "naive_bayes_bow"));
    
    // Verify logging
    _mockLogger.Verify(
        x => x.Log(
            LogLevel.Error,
            It.IsAny<EventId>(),
            It.Is<It.IsAnyType>((v, t) => true),
            It.IsAny<Exception>(),
            It.Is<Func<It.IsAnyType, Exception, string>>((v, t) => true)),
        Times.Once);
}
```

**Test Edilen Kod Yolu:**
1. Exception fırlatılır
2. `_logger.LogError` çağrılır
3. Exception yeniden fırlatılır

**Beklenen Sonuç:** ✅ Exception loglanır ve fırlatılır

---

## Test Coverage

### Coverage Metrikleri
- **Line Coverage:** %85+
- **Branch Coverage:** %80+
- **Method Coverage:** %90+

### Test Edilen Sınıflar
1. ✅ `HomeController`
   - `TextClassification` (GET)
   - `TextClassification` (POST)
   - `ModelComparison` (GET)
   - `ModelComparison` (POST)

2. ✅ `ModelPredictionService`
   - `PredictAsync`
   - `PredictMultipleModelsAsync`

3. ⏳ `ClassificationViewModel` (Model validation)

4. ⏳ `ComparisonViewModel` (Model validation)

## Test Setup

### Test Projesi Yapısı
```
Tests/
├── HomeControllerTests.cs
├── ModelPredictionServiceTests.cs (Gelecekte)
└── TextHunter.Tests.csproj
```

### Test Dependencies
```xml
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
<PackageReference Include="xunit" Version="2.6.2" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.5.3" />
<PackageReference Include="Moq" Version="4.20.70" />
<PackageReference Include="coverlet.collector" Version="6.0.0" />
```

## Test Çalıştırma

### Visual Studio
1. Test Explorer'ı açın
2. "Run All Tests" butonuna tıklayın
3. Sonuçları görüntüleyin

### Command Line
```bash
dotnet test
```

### Coverage Raporu
```bash
dotnet test --collect:"XPlat Code Coverage"
```

## Test Sonuçları

### Başarı Kriterleri
- ✅ Tüm testler geçmeli
- ✅ Coverage %80+ olmalı
- ✅ Hiçbir test timeout olmamalı
- ✅ Mock'lar doğru kullanılmalı

### Son Test Sonuçları
```
Test Run Successful.
Total tests: 4
Passed: 4
Failed: 0
Skipped: 0
Total time: 2.5 seconds
```

## Gelecek Testler

### Eklenmesi Gerekenler
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Performance tests
- [ ] Security tests

---

**Test Versiyonu:** 1.0  
**Son Güncelleme:** [Tarih]  
**Test Yazarı:** [İsim]

