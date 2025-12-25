# 📋 Benim Görevlerim - TextHunter Projesi

## 🎯 Proje Özeti

**Proje Adı:** Human or AI - Makale Özetleri Üzerinden Metin Tespiti  
**Proje Teslimi:** 19 Aralık 2025 veya 26 Aralık 2025  
**Dönem Notuna Etkisi:** %40

---

## 👨‍💻 Bana Düşen Görevler

| User Story | Görev | Puan | Durum |
|------------|-------|------|-------|
| **US-1** | Veri Seti Toplama | 5 puan | ✅ Tamamlandı |
| **US-2** | Veri Temizleme (EDA) | 5 puan | ⏳ Devam Ediyor |
| **US-3** | Model Eğitimi (3 farklı ML) | 10 puan | 🔄 Hazır |
| - | White Box Testler | - | 📝 Yapılacak |
| - | Kod Kalite Analizi (SonarQube) | - | 📝 Yapılacak |

**Toplam Puan:** 20 puan (maksimum)

---

## 📁 User Story-1: Veri Seti Toplama (5 Puan) ✅

### Gereksinimler
- ✅ En az 6000 örnek veri
- ✅ 3000 insan yazımı makale özeti
- ✅ 3000 AI (Gemini) yazımı metin
- ✅ ArXiv sitesinden veri toplama
- ✅ Uygun lisans kontrolü (MIT, Apache 2.0, BSD, CC-BY, CC0)

### Mevcut Durum
```
📊 Veri İstatistikleri:
- Toplam Örnek: ~19.472
- Human Örnekleri: Yüklendi ✅
- AI Örnekleri: Yüklendi ✅
- Format: CSV ve JSON
```

### İlgili Dosyalar
| Dosya | Açıklama |
|-------|----------|
| `Scripts/data_collection.py` | Ana veri toplama scripti |
| `Scripts/data_collection/collect_arxiv_data.py` | ArXiv'den veri toplama |
| `Scripts/generate_ai_data.py` | Gemini AI ile metin üretimi |
| `Data/raw/combined_dataset.csv` | Birleştirilmiş veri seti |
| `Data/raw/human_abstracts.csv` | İnsan yazımı özetler |
| `Data/raw/ai_abstracts.csv` | AI yazımı metinler |

### Nasıl Çalıştırılır?

```powershell
# 1. Gerekli paketleri yükle
cd Scripts
pip install -r requirements.txt

# 2. Gemini API anahtarını ayarla
$env:GEMINI_API_KEY="your-api-key-here"

# 3. Veri toplama scriptini çalıştır
python data_collection.py
```

---

## 📁 User Story-2: Veri Temizleme / EDA (5 Puan) ⏳

### Gereksinimler
- ⏳ Veri temizleme (null değerler, duplikasyonlar)
- ⏳ Metin normalizasyonu
- ⏳ EDA (Exploratory Data Analysis)
- ⏳ Veri dengeleme

### İlgili Dosyalar
| Dosya | Açıklama |
|-------|----------|
| `Scripts/data_cleaning.py` | Veri temizleme scripti |
| `Data/cleaned/` | Temizlenmiş veri klasörü |

### Nasıl Çalıştırılır?

```powershell
cd Scripts
python data_cleaning.py
```

### Temizleme İşlemleri

1. **Metin Normalizasyonu:**
   - Küçük harfe çevirme
   - URL'leri kaldırma
   - Email adreslerini kaldırma
   - Fazla boşlukları temizleme

2. **Duplikasyon Kontrolü:**
   - Tekrarlanan metinleri kaldırma
   - Benzersiz metin kontrolü

3. **Veri Doğrulama:**
   - Minimum metin uzunluğu: 50 karakter
   - Maksimum metin uzunluğu: 5000 karakter
   - Label kontrolü (Human/AI)

4. **Veri Dengeleme:**
   - Human ve AI sınıflarını eşitleme

### EDA (Exploratory Data Analysis) İçin Yapılacaklar

```python
# EDA için örnek kod
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veri yükle
df = pd.read_csv('../Data/raw/combined_dataset.csv')

# Temel istatistikler
print(df.describe())
print(df['label'].value_counts())

# Metin uzunluğu dağılımı
df['text_length'] = df['text'].str.len()
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='text_length', hue='label', bins=50)
plt.title('Metin Uzunluğu Dağılımı')
plt.savefig('../Documentation/eda_text_length.png')

# Word count dağılımı
df['word_count'] = df['text'].str.split().str.len()
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='word_count', hue='label', bins=50)
plt.title('Kelime Sayısı Dağılımı')
plt.savefig('../Documentation/eda_word_count.png')
```

---

## 📁 User Story-3: Model Eğitimi (10 Puan) 🔄

### Gereksinimler
- ✅ 3 farklı ML algoritması ile model eğitimi
- ✅ Naive Bayes modeli
- ✅ Random Forest modeli
- ✅ SVM modeli

### Eğitilecek Modeller

| Model | Vectorizer | Açıklama |
|-------|------------|----------|
| Naive Bayes | BoW | Bag of Words ile Naive Bayes |
| Naive Bayes | TF-IDF | TF-IDF ile Naive Bayes |
| Random Forest | BoW | Bag of Words ile Random Forest |
| Random Forest | TF-IDF | TF-IDF ile Random Forest |
| SVM | BoW | Bag of Words ile SVM |
| SVM | TF-IDF | TF-IDF ile SVM |

### İlgili Dosyalar
| Dosya | Açıklama |
|-------|----------|
| `Scripts/train_models.py` | Model eğitim scripti |
| `MLModels/` | Eğitilmiş modeller klasörü |

### Nasıl Çalıştırılır?

```powershell
cd Scripts
python train_models.py
```

### Eğitim Çıktıları
Eğitim sonrası `MLModels/` klasöründe:
- `naive_bayes_bow_model.pkl`
- `naive_bayes_bow_vectorizer.pkl`
- `naive_bayes_tfidf_model.pkl`
- `naive_bayes_tfidf_vectorizer.pkl`
- `random_forest_bow_model.pkl`
- `random_forest_bow_vectorizer.pkl`
- `random_forest_tfidf_model.pkl`
- `random_forest_tfidf_vectorizer.pkl`
- `svm_bow_model.pkl`
- `svm_bow_vectorizer.pkl`
- `svm_tfidf_model.pkl`
- `svm_tfidf_vectorizer.pkl`
- `training_results.json` (Eğitim metrikleri)

### Model Performans Metrikleri

Her model için kaydedilen metrikler:
- **Accuracy:** Doğruluk oranı
- **Precision:** Kesinlik
- **Recall:** Duyarlılık
- **F1-Score:** F1 skoru
- **Confusion Matrix:** Karışıklık matrisi

---

## 🧪 White Box Testler

### Test Dosyası Konumu
- `Tests/` klasörü
- `Documentation/WHITE_BOX_TESTLER.md`

### Yapılacak Test Türleri

1. **Statement Coverage (Deyim Kapsama):**
   - Her kod satırının en az bir kez çalıştırılması
   
2. **Branch Coverage (Dal Kapsama):**
   - Her if/else dalının test edilmesi
   
3. **Path Coverage (Yol Kapsama):**
   - Farklı kod yollarının test edilmesi

### Test Edilecek Fonksiyonlar

```python
# data_cleaning.py
- clean_text()
- remove_duplicates()
- balance_dataset()
- validate_data()

# train_models.py
- load_data()
- train_naive_bayes()
- train_random_forest()
- train_svm()
```

### Örnek Test Kodu

```python
import pytest
from Scripts.data_cleaning import clean_text, remove_duplicates

class TestDataCleaning:
    def test_clean_text_removes_urls(self):
        text = "Check this https://example.com link"
        result = clean_text(text)
        assert "https://" not in result
    
    def test_clean_text_removes_emails(self):
        text = "Contact test@email.com for info"
        result = clean_text(text)
        assert "@" not in result
    
    def test_clean_text_short_text_returns_empty(self):
        text = "Short"
        result = clean_text(text)
        assert result == ""
    
    def test_remove_duplicates(self):
        data = [
            {"text": "Same text"},
            {"text": "Same text"},
            {"text": "Different text"}
        ]
        result = remove_duplicates(data)
        assert len(result) == 2
```

---

## 📊 Kod Kalite Analizi (SonarQube)

### SonarQube Kurulumu

```powershell
# SonarQube Docker ile çalıştırma
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# SonarScanner kurulumu
# https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
```

### sonar-project.properties

```properties
sonar.projectKey=texthunter
sonar.projectName=TextHunter
sonar.projectVersion=1.0
sonar.sources=.
sonar.sourceEncoding=UTF-8
sonar.language=py,cs
sonar.python.version=3.11
```

### Analiz Çalıştırma

```powershell
sonar-scanner
```

### Kontrol Edilecek Metrikler
- **Code Smells:** Kod kokuları
- **Bugs:** Hata sayısı
- **Vulnerabilities:** Güvenlik açıkları
- **Code Coverage:** Test kapsama oranı
- **Duplications:** Tekrarlanan kod yüzdesi

---

## 📅 İş Planı / Timeline

### Hafta 1 (Mevcut)
- [x] Veri seti toplama
- [x] Temel proje yapısı
- [ ] Veri temizleme
- [ ] EDA

### Hafta 2
- [ ] Model eğitimi
- [ ] White box testler
- [ ] Kod kalite analizi

### Teslim Öncesi
- [ ] Dokümantasyon kontrolü
- [ ] Test sonuçları
- [ ] Final kontrol

---

## 🔗 Arkadaşıma Düşen Görevler (Referans)

| User Story | Görev | Puan |
|------------|-------|------|
| US-4 | Model Entegrasyonu | 10 puan |
| US-5 | Sonuç Gösterimi (3 model, yüzdeler) | 10 puan |
| - | Arayüz (UI) | - |
| - | Dokümantasyon Paketi | - |
| - | Test Cases | - |

**Not:** Çoklu model desteği olmazsa -5 puan!

---

## 📝 Notlar

### API Anahtarı
Gemini API anahtarı için: https://makersuite.google.com/app/apikey

### Gerekli Paketler
```
requests>=2.31.0
beautifulsoup4>=4.12.0
arxiv>=2.1.0
google-generativeai>=0.3.0
pandas>=2.0.0
numpy>=1.24.0
tqdm>=4.66.0
scikit-learn>=1.3.0
joblib>=1.3.0
nltk>=3.8.0
```

### Proje Yapısı
```
TextHunter/
├── Scripts/                 # Python scriptleri (BENİM)
│   ├── data_collection.py   # Veri toplama
│   ├── data_cleaning.py     # Veri temizleme
│   └── train_models.py      # Model eğitimi
├── Data/                    # Veri klasörleri
│   ├── raw/                 # Ham veri
│   ├── cleaned/             # Temizlenmiş veri
│   └── processed/           # İşlenmiş veri
├── MLModels/                # Eğitilmiş modeller
├── Tests/                   # Testler
├── Documentation/           # Dokümantasyon
├── Controllers/             # ASP.NET Controller'lar (ARKADAŞ)
├── Views/                   # Razor Views (ARKADAŞ)
└── Services/               # ML Servisler (ARKADAŞ)
```

---

**Son Güncelleme:** 17 Aralık 2025

