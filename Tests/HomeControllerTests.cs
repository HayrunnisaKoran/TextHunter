using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Moq;
using TextHunter.Controllers;
using TextHunter.Models;
using TextHunter.Services;
using Xunit;

namespace TextHunter.Tests
{
    public class HomeControllerTests
    {
        private readonly Mock<ILogger<HomeController>> _mockLogger;
        private readonly Mock<IModelPredictionService> _mockPredictionService;
        private readonly HomeController _controller;

        public HomeControllerTests()
        {
            _mockLogger = new Mock<ILogger<HomeController>>();
            _mockPredictionService = new Mock<IModelPredictionService>();
            _controller = new HomeController(_mockLogger.Object, _mockPredictionService.Object);
        }

        [Fact]
        public void TextClassification_Get_ReturnsView()
        {
            // Act
            var result = _controller.TextClassification();

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            var model = Assert.IsType<ClassificationViewModel>(viewResult.Model);
            Assert.NotNull(model);
            Assert.True(model.AvailableModels.Count > 0);
        }

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
        }

        [Fact]
        public void ModelComparison_Get_ReturnsView()
        {
            // Act
            var result = _controller.ModelComparison();

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            var model = Assert.IsType<ComparisonViewModel>(viewResult.Model);
            Assert.NotNull(model);
        }

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

        [Fact]
        public async Task ModelComparison_Post_WithEmptyText_ReturnsViewWithError()
        {
            // Arrange
            var viewModel = new ComparisonViewModel
            {
                Text = ""
            };

            // Act
            var result = await _controller.ModelComparison(viewModel);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            var model = Assert.IsType<ComparisonViewModel>(viewResult.Model);
            Assert.False(_controller.ModelState.IsValid);
        }
    }
}

