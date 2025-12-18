# Veri Seti Toplama Scripti

Bu script, proje için gerekli veri setini toplar.

## Gereksinimler

```bash
pip install -r requirements.txt
```

## Kullanım

### 1. Gemini API Anahtarı Ayarlama

Gemini API anahtarınızı ortam değişkeni olarak ayarlayın:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 2. Script Çalıştırma

```bash
cd Scripts
python data_collection.py
```

## Çıktılar

Script şu dosyaları oluşturur:
- `Data/raw/human_abstracts.json` - ArXiv'den toplanan insan yazımı özetler
- `Data/raw/human_abstracts.csv` - CSV formatında
- `Data/raw/ai_abstracts.json` - Gemini AI ile üretilen metinler
- `Data/raw/ai_abstracts.csv` - CSV formatında
- `Data/raw/combined_dataset.json` - Birleştirilmiş veri seti
- `Data/raw/combined_dataset.csv` - CSV formatında

## Notlar

- ArXiv API rate limiting nedeniyle toplama işlemi zaman alabilir
- Gemini API kullanımı için ücretsiz API anahtarı alabilirsiniz: https://makersuite.google.com/app/apikey
- Veri toplama işlemi kesilirse, script tekrar çalıştırıldığında mevcut verilerin üzerine yazılır

