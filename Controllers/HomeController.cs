using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using TextHunter.Models;
using TextHunter.Services;

namespace TextHunter.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly IModelPredictionService _predictionService;

        public HomeController(ILogger<HomeController> logger, IModelPredictionService predictionService)
        {
            _logger = logger;
            _predictionService = predictionService;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult TextClassification()
        {
            var model = new ClassificationViewModel
            {
                AvailableModels = new List<string>
                {
                    "naive_bayes_bow",
                    "naive_bayes_tfidf",
                    "random_forest_bow",
                    "random_forest_tfidf",
                    "svm_bow",
                    "svm_tfidf"
                }
            };
            return View(model);
        }

        [HttpPost]
        public async Task<IActionResult> TextClassification(ClassificationViewModel model)
        {
            if (string.IsNullOrWhiteSpace(model.Text))
            {
                ModelState.AddModelError("Text", "Lütfen bir metin girin.");
                model.AvailableModels = new List<string>
                {
                    "naive_bayes_bow",
                    "naive_bayes_tfidf",
                    "random_forest_bow",
                    "random_forest_tfidf",
                    "svm_bow",
                    "svm_tfidf"
                };
                return View(model);
            }

            try
            {
                model.Result = await _predictionService.PredictAsync(model.Text, model.SelectedModel);
                model.AvailableModels = new List<string>
                {
                    "naive_bayes_bow",
                    "naive_bayes_tfidf",
                    "random_forest_bow",
                    "random_forest_tfidf",
                    "svm_bow",
                    "svm_tfidf"
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Tahmin yapılırken hata oluştu");
                ModelState.AddModelError("", "Tahmin yapılırken bir hata oluştu. Lütfen tekrar deneyin.");
                model.AvailableModels = new List<string>
                {
                    "naive_bayes_bow",
                    "naive_bayes_tfidf",
                    "random_forest_bow",
                    "random_forest_tfidf",
                    "svm_bow",
                    "svm_tfidf"
                };
            }

            return View(model);
        }

        public IActionResult ModelComparison()
        {
            var model = new ComparisonViewModel();
            return View(model);
        }

        [HttpPost]
        public async Task<IActionResult> ModelComparison(ComparisonViewModel model)
        {
            if (string.IsNullOrWhiteSpace(model.Text))
            {
                ModelState.AddModelError("Text", "Lütfen bir metin girin.");
                return View(model);
            }

            try
            {
                model.Results = await _predictionService.PredictMultipleModelsAsync(model.Text);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Tahmin yapılırken hata oluştu");
                ModelState.AddModelError("", "Tahmin yapılırken bir hata oluştu. Lütfen tekrar deneyin.");
            }

            return View(model);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
