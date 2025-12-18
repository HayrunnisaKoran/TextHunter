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

- 🤖 **3 Farklı ML Modeli:** Naive Bayes, Random Forest, SVM
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
| Naive Bayes | BoW | `naive_bayes_bow_model.pkl` |
| Naive Bayes | TF-IDF | `naive_bayes_tfidf_model.pkl` |
| Random Forest | BoW | `random_forest_bow_model.pkl` |
| Random Forest | TF-IDF | `random_forest_tfidf_model.pkl` |
| SVM | BoW | `svm_bow_model.pkl` |
| SVM | TF-IDF | `svm_tfidf_model.pkl` |

### Performans Metrikleri

Model eğitimi sonrası `MLModels/training_results.json` dosyasında:
- Accuracy (Doğruluk)
- Precision (Kesinlik)
- Recall (Duyarlılık)
- F1-Score
- Confusion Matrix

---

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

### Örnek Kullanım

1. "Model Comparison" sayfasına gidin
2. Analiz edilecek metni girin
3. "Analyze" butonuna tıklayın
4. 3 farklı modelin Human/AI yüzde tahminlerini görün

---

## 🧪 Test

### Unit Testleri Çalıştırma

```bash
cd Tests
dotnet test
```

### White Box Test Dokümantasyonu

Detaylı test senaryoları için: `Documentation/WHITE_BOX_TESTLER.md`

---

## 📚 Dokümantasyon

| Dosya | İçerik |
|-------|--------|
| [BENIM_GOREVLERIM.md](Documentation/BENIM_GOREVLERIM.md) | Veri toplama, temizleme ve model eğitimi görevleri |
| [USER_STORY_1_DURUM.md](Documentation/USER_STORY_1_DURUM.md) | Veri seti toplama durumu |
| [USER_STORY_2_3_4_DURUM.md](Documentation/USER_STORY_2_3_4_DURUM.md) | Diğer user story'lerin durumu |
| [WHITE_BOX_TESTLER.md](Documentation/WHITE_BOX_TESTLER.md) | White box test senaryoları |
| [SONARQUBE_ANALIZ.md](Documentation/SONARQUBE_ANALIZ.md) | Kod kalite analizi |
| [UI_UX_TASARIM.md](Documentation/UI_UX_TASARIM.md) | Arayüz tasarım dökümanı |
| [SOZLESME_YAZILIM_SARTNAMESI.md](Documentation/SOZLESME_YAZILIM_SARTNAMESI.md) | Yazılım şartnamesi |

---

## 👥 Ekip

| Görev | Sorumluluklar |
|-------|---------------|
| **Kişi 1** | Veri Toplama, Veri Temizleme/EDA, Model Eğitimi, White Box Testler, Kod Kalite Analizi |
| **Kişi 2** | Model Entegrasyonu, Arayüz (UI), Sonuç Gösterimi, Dokümantasyon Paketi, Test Cases |

---

## 📄 User Stories

| US | Açıklama | Puan |
|----|----------|------|
| US-1 | Veri Seti Toplama (6000 örnek) | 5 |
| US-2 | Veri Temizleme | 5 |
| US-3 | Model Eğitimi (3 farklı ML) | 10 |
| US-4 | Model Entegrasyonu (Çoklu model desteği) | 10 |
| US-5 | Sonuç Gösterimi (Yüzdelik oranlar) | 10 |
| **Toplam** | | **40** |

> ⚠️ Çoklu model desteği yoksa -5 puan!

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

**📅 Son Güncelleme:** 17 Aralık 2025
