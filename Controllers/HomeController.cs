using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using TextHunter.Data;
using TextHunter.Models;
using TextHunter.Services;
using Microsoft.AspNetCore.Http;

namespace TextHunter.Controllers
{
    public class HomeController : Controller
    {
        private readonly IInputSanitizerService _sanitizer;
        private readonly ILogger<HomeController> _logger;
        private readonly IModelPredictionService _predictionService;
        private readonly AppDbContext _context;
        public HomeController(ILogger<HomeController> logger, IModelPredictionService predictionService, IInputSanitizerService sanitizer, AppDbContext context)
        {
            _logger = logger;
            _predictionService = predictionService;
            _sanitizer = sanitizer;
            _context = context; // Veritabanı bağlantımız hazır!
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

            // ANALİZDEN ÖNCE TEMİZLİK YAP:
            model.Text = _sanitizer.Sanitize(model.Text);

            // Şimdi güvenli metni servise gönder
            var result = await _predictionService.PredictAsync(model.Text, model.SelectedModel);

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

        public IActionResult Profile()
        {
            // Session'dan kullanıcı ID'sini kontrol et
            var userId = HttpContext.Session.GetInt32("UserId");
            if (!userId.HasValue)
            {
                TempData["ErrorMessage"] = "Profil sayfasına erişmek için giriş yapmanız gerekiyor.";
                return RedirectToAction("Login");
            }

            return View();
        }

        [HttpPost]
        public async Task<IActionResult> UpdateProfile(string FullName, string Email)
        {
            // Session'dan kullanıcı ID'sini al
            var userId = HttpContext.Session.GetInt32("UserId");
            if (!userId.HasValue)
            {
                TempData["ErrorMessage"] = "İşlem yapmak için giriş yapmanız gerekiyor.";
                return RedirectToAction("Login");
            }

            // Input validasyonu
            if (string.IsNullOrWhiteSpace(FullName))
            {
                ModelState.AddModelError("FullName", "Ad Soyad gereklidir.");
            }
            if (string.IsNullOrWhiteSpace(Email))
            {
                ModelState.AddModelError("Email", "E-posta gereklidir.");
            }

            if (!ModelState.IsValid)
            {
                return View("Profile");
            }

            // Veritabanından kullanıcıyı bul
            var user = await _context.Users.FindAsync(userId.Value);
            if (user == null)
            {
                TempData["ErrorMessage"] = "Kullanıcı bulunamadı.";
                return RedirectToAction("Login");
            }

            // Email değiştiyse, başka bir kullanıcıda aynı email var mı kontrol et
            if (user.Email != Email && _context.Users.Any(u => u.Email == Email && u.Id != userId.Value))
            {
                ModelState.AddModelError("Email", "Bu e-posta adresi zaten kullanımda.");
                return View("Profile");
            }

            // Kullanıcı bilgilerini güncelle
            user.FullName = FullName;
            user.Email = Email;
            
            await _context.SaveChangesAsync();

            // Session'ı güncelle
            HttpContext.Session.SetString("UserFullName", FullName);
            HttpContext.Session.SetString("UserEmail", Email);

            TempData["SuccessMessage"] = "Profil bilgileriniz başarıyla güncellendi!";
            return RedirectToAction("Profile");
        }

        public IActionResult Settings()
        {
            return View();
        }

        [HttpPost]
        public IActionResult UpdateSettings(bool? DarkMode, bool? EmailNotifications)
        {
            // Session'dan kullanıcı ID'sini kontrol et
            var userId = HttpContext.Session.GetInt32("UserId");
            if (!userId.HasValue)
            {
                TempData["ErrorMessage"] = "Ayarları değiştirmek için giriş yapmanız gerekiyor.";
                return RedirectToAction("Login");
            }

            // Ayarları session'a kaydet
            HttpContext.Session.SetString("DarkMode", DarkMode == true ? "true" : "false");
            HttpContext.Session.SetString("EmailNotifications", EmailNotifications == true ? "true" : "false");

            TempData["SuccessMessage"] = "Ayarlarınız başarıyla kaydedildi!";
            return RedirectToAction("Settings");
        }

        public IActionResult Privacy()
        {
            return View();
        }

        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Login(string Email, string Password)
        {
            // 1. Input validasyonu
            if (string.IsNullOrWhiteSpace(Email))
            {
                ModelState.AddModelError("Email", "E-posta gereklidir.");
            }
            if (string.IsNullOrWhiteSpace(Password))
            {
                ModelState.AddModelError("Password", "Şifre gereklidir.");
            }

            if (!ModelState.IsValid)
            {
                return View();
            }

            // 2. Kullanıcının şifresini hashle (Veritabanındakiyle karşılaştırmak için)
            string hashedPassword = HashPassword(Password);

            // 3. Veritabanında bu email ve şifreye sahip kullanıcı var mı?
            var user = _context.Users.FirstOrDefault(u => u.Email == Email && u.PasswordHash == hashedPassword);

            if (user != null)
            {
                // GİRİŞ BAŞARILI
                // Session'a kullanıcı bilgilerini kaydet
                HttpContext.Session.SetInt32("UserId", user.Id);
                HttpContext.Session.SetString("UserFullName", user.FullName);
                HttpContext.Session.SetString("UserEmail", user.Email);
                
                TempData["SuccessMessage"] = $"Hoş geldiniz, {user.FullName}!";
                return RedirectToAction("Index");
            }
            else
            {
                // GİRİŞ HATALI
                ModelState.AddModelError("", "E-posta veya şifre hatalı.");
                return View();
            }
        }

        public IActionResult Register()
        {
            return View();
        }


        [HttpPost]
        public async Task<IActionResult> Register(string FullName, string Email, string Password)
        {
            // 1. Input validasyonu
            if (string.IsNullOrWhiteSpace(FullName))
            {
                ModelState.AddModelError("FullName", "Ad Soyad gereklidir.");
            }
            if (string.IsNullOrWhiteSpace(Email))
            {
                ModelState.AddModelError("Email", "E-posta gereklidir.");
            }
            if (string.IsNullOrWhiteSpace(Password))
            {
                ModelState.AddModelError("Password", "Şifre gereklidir.");
            }

            if (!ModelState.IsValid)
            {
                return View();
            }

            // 2. Email kontrolü (Aynı email ile iki kayıt olmasın - Veri Tutarlılığı)
            if (_context.Users.Any(u => u.Email == Email))
            {
                ModelState.AddModelError("Email", "Bu e-posta adresi zaten kullanımda.");
                return View();
            }

            // 3. Yeni kullanıcı nesnesi oluşturma
            var newUser = new User
            {
                FullName = FullName,
                Email = Email,
                PasswordHash = HashPassword(Password), // Güvenli şifreleme!
                CreatedAt = DateTime.UtcNow // PostgreSQL için UTC zaman kullan
            };

            // 4. Veritabanına kaydetme
            _context.Users.Add(newUser);
            await _context.SaveChangesAsync();

            // 4. Geri bildirim ve yönlendirme
            TempData["SuccessMessage"] = "Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.";
            return RedirectToAction("Login");
        }

        public IActionResult Logout()
        {
            // Session'ı temizle
            HttpContext.Session.Clear();
            
            TempData["SuccessMessage"] = "Başarıyla çıkış yaptınız!";
            return RedirectToAction("Index");
        }

        private string HashPassword(string password) //sifreleme adımı
        {
            if (string.IsNullOrEmpty(password))
            {
                throw new ArgumentException("Şifre boş olamaz.", nameof(password));
            }
            
            using (var sha256 = System.Security.Cryptography.SHA256.Create())
            {
                var bytes = sha256.ComputeHash(System.Text.Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(bytes);
            }
        }


        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
