# TextHunter - Proje Dokümantasyonu

Bu klasör, TextHunter projesinin tüm dokümantasyonunu içerir.

## Dokümantasyon Listesi

### 1. [Veri Toplama Kılavuzu](./VERI_TOPLAMA_KILAVUZU.md)
Veri seti toplama işleminin adım adım nasıl yapılacağını açıklar.
- ArXiv API kullanımı
- Gemini API kurulumu
- Veri toplama scripti çalıştırma
- Sorun giderme

### 2. [Sözleşme / Yazılım Şartnamesi](./SOZLESME_YAZILIM_SARTNAMESI.md)
Proje kapsamı, gereksinimler ve teslim kriterleri.
- Proje bilgileri
- Teknik gereksinimler
- Fonksiyonel gereksinimler
- Teslim gereksinimleri

### 3. [Task Board](./TASK_BOARD.md)
Proje yönetimi ve görev takibi.
- GitHub Projects kullanımı
- Sprint planlama
- Görev atama
- İlerleme takibi

### 4. [UI/UX Tasarım](./UI_UX_TASARIM.md)
Kullanıcı arayüzü ve kullanıcı deneyimi dokümantasyonu.
- Tasarım sistemi
- Component'ler
- Responsive design
- Yazılım geliştirme kalıpları

### 5. [White Box Testler](./WHITE_BOX_TESTLER.md)
White Box test senaryoları ve sonuçları.
- Test framework (xUnit)
- Test case'leri
- Test coverage
- Test sonuçları

### 6. [SonarQube Analiz](./SONARQUBE_ANALIZ.md)
Kod kalitesi analiz kılavuzu.
- SonarQube kurulumu
- Source Monitor kullanımı
- Analiz metrikleri
- İyileştirme önerileri

### 7. [Ek Uygulamalar](./EK_UYGULAMALAR.md)
Ek uygulamaların dokümantasyonu.
- Test Bird
- Snake Game
- XOX Game (Socket Programming)
- Kalıp Bulma
- Labirent ve Fare (2D Oyun)

## Hızlı Başlangıç

### 1. Veri Toplama
```bash
# API anahtarını ayarla
$env:GEMINI_API_KEY="your-api-key"

# Veri toplama scriptini çalıştır
cd Scripts
python data_collection.py
```

### 2. Veri Temizleme
```bash
cd Scripts
python data_cleaning.py
```

### 3. Model Eğitimi
```bash
cd Scripts
python train_models.py
```

### 4. Web Uygulaması
```bash
dotnet run
```

## Proje Yapısı

```
TextHunter/
├── Controllers/          # MVC Controllers
├── Models/               # ViewModels ve Data Models
├── Services/            # Business Logic Services
├── Views/               # Razor Views
├── Scripts/             # Python Scripts
│   ├── data_collection.py
│   ├── data_cleaning.py
│   ├── train_models.py
│   └── predict.py
├── Data/                # Veri Setleri
│   ├── raw/
│   ├── cleaned/
│   └── processed/
├── MLModels/            # Eğitilmiş Modeller
├── Tests/               # Test Dosyaları
└── Documentation/      # Bu Klasör
```

## İletişim

Sorularınız için:
- GitHub Issues
- E-posta: [E-posta adresi]
- Proje Yöneticisi: [İsim]

---

**Son Güncelleme:** [Tarih]  
**Proje Versiyonu:** 1.0

