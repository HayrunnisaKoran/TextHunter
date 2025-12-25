# 🔍 TextHunter - Human or AI Text Detection

[![.NET](https://img.shields.io/badge/.NET-8.0-512BD4?style=flat&logo=dotnet)](https://dotnet.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Makale özetleri üzerinden metin tespiti yapan bir web uygulaması. Girilen metnin **insan** mı yoksa **yapay zeka (AI)** tarafından mı yazıldığını 3 farklı Machine Learning modeli ile tespit eder.

![TextHunter Demo](Documentation/demo_screenshot.png)

---

## 📋 Proje Bilgileri

| Bilgi | Detay |
|-------|-------|
| **Proje Adı** | Human or AI - Makale Özetleri Üzerinden Metin Tespiti |
| **Ders** | Yazılım Mühendisliği |
| **Dönem** | 2024-2025 Güz |
| **Teslim Tarihi** | 19-26 Aralık 2025 |

---

## ✨ Özellikler

- 🤖 **3 Farklı ML Modeli:** Naive Bayes,Logistic Regression , SVM
- 📊 **Yüzdelik Tahmin:** Her model için Human/AI yüzde oranları
- 🔄 **Çoklu Model Karşılaştırma:** Tüm modellerin sonuçlarını tek ekranda görme
- 🌐 **Web Arayüzü:** Modern ve kullanıcı dostu ASP.NET Core MVC
- 📈 **6000+ Eğitim Verisi:** ArXiv + Gemini AI kaynaklı

---

## 🏗️ Proje Yapısı

```
TextHunter/
├── 📁 Controllers/           # MVC Controller'lar
├── 📁 Models/               # ViewModel ve Data Model'ler
├── 📁 Services/             # ML Model Prediction Servisleri
├── 📁 Views/                # Razor View'lar
├── 📁 Scripts/              # Python Scriptleri
│   ├── data_collection.py   # Veri toplama (ArXiv + Gemini)
│   ├── data_cleaning.py     # Veri temizleme ve EDA
│   ├── train_models.py      # Model eğitimi
│   └── predict.py           # Tahmin scripti
├── 📁 Data/                 # Veri setleri
│   ├── raw/                 # Ham veri (~19.000 örnek)
│   ├── cleaned/             # Temizlenmiş veri
│   └── processed/           # İşlenmiş veri
├── 📁 MLModels/             # Eğitilmiş ML modelleri (.pkl)
├── 📁 Tests/                # Unit ve White Box testler
├── 📁 Documentation/        # Proje dokümantasyonu
└── 📁 wwwroot/             # Statik dosyalar (CSS, JS)
```

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download)
- [Python 3.11+](https://python.org/)
- [Gemini API Key](https://makersuite.google.com/app/apikey) (veri toplama için)

### 1. Python Bağımlılıkları

```bash
cd Scripts
pip install -r requirements.txt
```

### 2. Veri Seti Toplama (Opsiyonel)

> ⚠️ Veri seti zaten `Data/raw/` klasöründe mevcut. Bu adım sadece yeni veri toplamak için gereklidir.

```powershell
# Gemini API anahtarını ayarla
$env:GEMINI_API_KEY="your-api-key-here"

# Veri toplama
cd Scripts
python data_collection.py
```

### 3. Veri Temizleme

```bash
cd Scripts
python data_cleaning.py
```

### 4. Model Eğitimi

```bash
cd Scripts
python train_models.py
```

### 5. Web Uygulamasını Çalıştırma

```bash
# Proje ana dizininde
dotnet run
```

Tarayıcıda: `https://localhost:5001` veya `http://localhost:5000`

---

## 🧠 Machine Learning Modelleri

### Eğitilen Modeller

| Model | Vectorizer | Dosya |
|-------|------------|-------|
| Naive Bayes | BoW | `naive_bayes.pkl` |
| Logistic Regression | BoW | `logistic_regression.pkl` |
| SVM | BoW | `svm_model.pkl` |



## 📊 Veri Seti

### Kaynak Bilgileri

| Kaynak | Tür | Sayı | Lisans |
|--------|-----|------|--------|
| ArXiv | Human | 3000+ | CC-BY |
| Gemini AI | AI | 3000+ | - |

### Veri Formatı

```csv
text,label,source,arxiv_id,title,authors,published,license,collected_date,prompt,generated_date
"Abstract text...",Human,arxiv,http://arxiv.org/abs/...,Title,Authors,2025-...,CC-BY,2025-...,
"Generated text...",AI,gemini,,,,,,prompt text,2025-...
```

---

## 🖥️ Web Arayüzü

### Sayfalar

1. **Ana Sayfa:** Proje hakkında bilgi
2. **Text Classification:** Tek model ile metin sınıflandırma
3. **Model Comparison:** Tüm modellerin karşılaştırmalı sonuçları
4. **Profilim:** Kullanıcının isim, şifre ve e-posta bilgilerini güncellemesi seçenekleri
5. **Ayarlar:** Uygulama temasını değiştirme ve e-posta bildirimi yönetimi
6. **Giriş Sayfası:** Kayıtlı kullanıcı için giriş ekranı
7. **Kayıt Sayfası:** Kayıtlı olmayan kullanıcı için kayıt sayfası

### Örnek Kullanım

1. "Model Comparison" sayfasına gidin
2. Analiz edilecek metni girin
3. "Analiz Et" butonuna tıklayın
4. 3 farklı modelin Human/AI yüzde tahminlerini görün

---

## 🧪 Test

### Unit Testleri Çalıştırma

```bash
cd Tests
dotnet test
```

### White Box Test Dokümantasyonu

Tests klasöründe: 
-AccountIntegrationTests.cs
-DatabaseIntegrationTests.cs
-HomeControllerTests.cs
-ModelPredictionServiceTest.cs
-SecurityIntegrationTests.cs
test kodlarına ulaşılabilir
---


## 👥 Ekip

| Görev | Sorumluluklar |
|-------|---------------|
| **Hayrünnisa Koran** | Veri Toplama, Veri Temizleme/EDA, Model Eğitimi, Black Box Testler, SonarCube-Kod Kalite Analizi |
| **Filiz Kalmış** | Model Entegrasyonu, Arayüz (UI), Sonuç Gösterimi, Dokümantasyon Paketi, White box testleri |

---

## 🔧 Teknolojiler

### Backend
- ASP.NET Core MVC (.NET 8.0)
- C#

### Machine Learning
- Python 3.11+
- scikit-learn
- pandas, numpy
- NLTK

### Frontend
- Bootstrap 5
- Razor Pages
- jQuery

### Veri Kaynakları
- ArXiv API
- Google Gemini API

---

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- [ArXiv](https://arxiv.org/) - Açık erişimli makale özetleri
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI metin üretimi
- [scikit-learn](https://scikit-learn.org/) - ML kütüphanesi

---

**📅 Son Güncelleme:** 25 Aralık 2025
