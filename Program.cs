using TextHunter.Services;
using Microsoft.EntityFrameworkCore;
using TextHunter.Data;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Session yapılandırması
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// ML Model Prediction Service
builder.Services.AddScoped<IModelPredictionService, ModelPredictionService>();



//veritabani baglantisi
// ConnectionString'i al
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// Eğer bulunamazsa, alternatif yöntemlerle dene
if (string.IsNullOrEmpty(connectionString))
{
     connectionString = builder.Configuration["ConnectionStrings:DefaultConnection"];
}

// Hala bulunamazsa, manuel olarak hardcode et (GEÇİCİ ÇÖZÜM - DEBUG İÇİN)
if (string.IsNullOrEmpty(connectionString))
{
    // Build output'taki dosyaları kontrol et
    var basePath = builder.Environment.ContentRootPath;
    var appsettingsPath = Path.Combine(basePath, "appsettings.json");
    var appsettingsDevPath = Path.Combine(basePath, "appsettings.Development.json");
    
    // Dosyalar var mı kontrol et
    var filesExist = $"appsettings.json: {File.Exists(appsettingsPath)}, appsettings.Development.json: {File.Exists(appsettingsDevPath)}";
    
    // Geçici olarak hardcode connection string kullan
    connectionString = "Host=localhost;Port=5432;Database=TextHunterDB;Username=postgres;Password=postGRE123.";
    
    // UYARI: Bu geçici bir çözüm, asıl sorunu bulmalıyız
    System.Diagnostics.Debug.WriteLine($"UYARI: ConnectionString config'den okunamadı, hardcode değer kullanılıyor. Dosyalar: {filesExist}");
}
if (string.IsNullOrEmpty(connectionString))
{
    throw new Exception("ConnectionString hiçbir yöntemle bulunamadı!");
}


builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

var app = builder.Build();
// Debug i�in: E�er ba�lant� c�mlesi gelmiyorsa uygulamay� burada durdur ve uyar


// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseSession(); // Session middleware'i ekle

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
