# Sözleşme - Yazılım Şartnamesi

## Proje Bilgileri

**Proje Adı:** TextHunter - Human or AI Text Detection  
**Proje Tipi:** Makale Özetleri Üzerinden Metin Tespiti  
**Proje Süresi:** Güz Dönemi 2025  
**Teslim Tarihi:** 19 Aralık 2025 / 26 Aralık 2025  
**Proje Notu Etkisi:** %40  

## Proje Ekibi

- **Ekip Üyeleri:** [Hayrünnisa Koran - Filiz Kalmış]
- **Ekip Sayısı:** [2 kişi]
- **Proje Yöneticisi:** [Hayrünnisa Koran]

## Proje Kapsamı

### Amaç
Makale özetleri üzerinden metinlerin insan mı yoksa AI tarafından mı yazıldığını tespit eden bir web uygulaması geliştirmek.

### Kapsam İçi
1. Veri seti toplama (6000 örnek: 3000 Human + 3000 AI)
2. Veri temizleme ve ön işleme
3. 3 farklı ML algoritması ile model eğitimi
4. Model entegrasyonu ve web uygulaması
5. Çoklu model desteği ile tahmin yapma
6. Yüzdelik olasılık gösterimi
7. Test case'leri ve dokümantasyon

### Kapsam Dışı
- Deep Learning modelleri (opsiyonel User Story-7)
- Transform Learning modelleri (opsiyonel User Story-7)
- Mobil uygulama geliştirme
- API servisi geliştirme

## Teknik Gereksinimler

### Backend
- **Framework:** ASP.NET Core MVC (.NET 8.0)
- **Dil:** C#
- **Mimari:** N-Katmanlı Mimari (N-Layered Architecture)
- **Design Pattern:** Singleton, Dependency Injection

### Machine Learning
- **Dil:** Python 3.8+
- **Kütüphaneler:** scikit-learn, pandas, numpy, joblib, nltk
- **Algoritmalar:** 
  - Naive Bayes (BoW ve TF-IDF)
  - Random Forest (BoW ve TF-IDF)
  - SVM (BoW ve TF-IDF)

### Frontend
- **Framework:** Bootstrap 5
- **View Engine:** Razor Pages
- **JavaScript:** jQuery (validation için)

### Veri Toplama
- **Kaynak 1:** ArXiv API (insan yazımı özetler)
- **Kaynak 2:** Google Gemini API (AI yazımı metinler)
- **Lisans:** MIT, Apache 2.0, BSD, CC-BY, CC0

### Veritabanı
- Model dosyaları: Pickle formatında dosya sistemi
- Veri setleri: JSON ve CSV formatında dosya sistemi

## Fonksiyonel Gereksinimler

### User Story-1: Veri Seti Toplama (5 puan)
- **Gereksinim:** En az 6000 örnek kod (3000 Human + 3000 AI)
- **Kaynak:** ArXiv ve Gemini API
- **Lisans:** MIT, Apache 2.0, BSD, CC-BY, CC0
- **Durum:** ✅ Tamamlandı

### User Story-2: Veri Temizleme (5 puan)
- **Gereksinim:** Ham veriyi temizleme, normalize etme, tokenizasyon
- **Çıktı:** Temizlenmiş veri seti
- **Durum:** ✅ Tamamlandı

### User Story-3: Model Eğitimi (10 puan)
- **Gereksinim:** 3 farklı ML algoritması ile model eğitimi
- **Algoritmalar:** Naive Bayes, Random Forest, SVM
- **Vectorizer:** BoW ve TF-IDF (her algoritma için)
- **Toplam Model:** 6 model (3 algoritma × 2 vectorizer)
- **Durum:** ✅ Tamamlandı

### User Story-4: Model Entegrasyonu (10 puan)
- **Gereksinim:** Modellerin yazılıma entegrasyonu
- **Çoklu Model Desteği:** Zorunlu (-5 puan yoksa)
- **Durum:** ✅ Tamamlandı

### User Story-5: Yüzdelik Olasılık Gösterimi (10 puan)
- **Gereksinim:** 3 farklı ML tahminleri ile yüzdelik oranları gösterme
- **Çıktı:** Her model için Human % ve AI % gösterimi
- **Durum:** ✅ Tamamlandı

### User Story-7: Opsiyonel - Deep Learning (Ödül İçin)
- **Gereksinim:** 
  - DL modelleri (CNN, LSTM, GRU, BiLSTM - en az 3)
  - Transform Learning (BERT, RoBERTa, CodeBERT - en az 1)
  - Hibrit yaklaşım (AutoML + ML/DL/TL)
  - Hyperparameter kayıtları
  - Metrikler (ACC, FM, Recall, Precision, Confusion Matrix)
  - ROC eğrisi görselleştirme
- **Durum:** ⏳ Opsiyonel

## Dokümantasyon Gereksinimleri

### Sözleşme/Yazılım Şartnamesi (5 puan)
- **Bu Doküman:** ✅ Tamamlandı

### Task Board (5 puan)
- **Gereksinim:** Scrum Table/Monday.com/GitHub Task Board/GitLab Task Board/BitBucket Task Board
- **Durum:** ✅ Dokümantasyon hazırlandı

### UI/UX Tasarımı (5 puan)
- **Gereksinim:** 
  - Rahat kullanılabilirlik
  - Göster tasarımı
  - Tasarım aracı kullanımı (Metro Framework, JavaFX, DevEx, Google Material)
  - Yazılım geliştirme kalıbı (N-Katmanlı mimari, Singleton)
  - Kod tekrarı kontrolü
  - Normalizasyon
- **Durum:** ✅ Dokümantasyon hazırlandı

### Test Caseler (10 puan)
- **Gereksinim:** STD Test Dökümanı, en az 5 test case
- **Durum:** ✅ 10 test case hazırlandı

### White Box Testler (10 puan)
- **Gereksinim:** En az 3 adet Selenium veya NUnit/XUnit test case
- **Durum:** ✅ NUnit testleri hazırlandı

### Yazılım Kalitesi (5 puan)
- **Gereksinim:** SonarQube veya Source Monitor analizi
- **Durum:** ✅ Kılavuz hazırlandı

## Ek Uygulamalar (20 puan - 4 adet)

### Ek-1: Test Bird (5 puan)
- **Gereksinim:** Giriş testi tamamlanıp, onay maili alındı mı?
- **Durum:** ⏳ Yapılacak

### Ek-2: Snake Game (5 puan)
- **Gereksinim:** Verilen VB kodu çalıştırılıp 6 adet test case çıkarıldı mı?
- **Durum:** ⏳ Yapılacak

### Ek-3: XOX Game (5 puan)
- **Gereksinim:** Socket Programlama barındıran uygulama yazılıp ek dosyası hazırlandı mı?
- **İçerik:** Amaç, girdiler, program kodu ve 3 adet test case tablosu
- **Durum:** ⏳ Yapılacak

### Ek-4: Kalıp Bulma (5 puan)
- **Gereksinim:** İstenen dizilime ait problem çözümü ve ek dosyalar hazırlandı mı?
- **İçerik:** Amaç, girdiler, program kodu ve 3 adet test case tablosu
- **Durum:** ⏳ Yapılacak

### Ek-5: Labirent ve Fare (5 puan)
- **Gereksinim:** 2D oyun yazılımı ve ek dosyalar hazırlandı mı?
- **Durum:** ⏳ Yapılacak

**Not:** 5 uygulamadan 4 adetinin yapılması yeterli (toplam 20 puan)

## Teslim Gereksinimleri

### Teslim Tarihleri
- **Normal Teslim:** 19 Aralık 2025 veya 26 Aralık 2025 (Cuma)
- **Geç Teslim:** 
  - 29 Aralık: -15 puan
  - 30 Aralık: -20 puan
  - 31 Aralık: -25 puan (son teslim)

### Teslim Formatı
- Proje kaynak kodu (GitHub/GitLab/BitBucket)
- Dokümantasyon klasörü
- Test dosyaları
- Ek uygulamalar
- Çalışan uygulama demo

## Kalite Standartları

### Kod Kalitesi
- Kod tekrarı yok
- Normalizasyon yapıldı
- Design pattern kullanıldı
- N-Katmanlı mimari uygulandı

### Test Kalitesi
- En az 5 test case (STD)
- En az 3 White Box test (NUnit/XUnit)
- Test coverage yeterli

### Dokümantasyon Kalitesi
- Tüm dokümanlar mevcut
- Açıklayıcı ve anlaşılır
- Güncel ve doğru

## Ceza Maddeleri

### Ek Madde-1: Hata Ceza Sistemi
- **Her bir hata:** -3 puan
- **Program çökerten hata:** -10 puan

### Ek Madde-2: Ekip Sayısı
- **Tek kişi proje:** -10 puan
- **4 kişi üzeri:** Alınan Not = (Proje notu × 4) / (Ekip kişi sayısı)

## Kabul Kriterleri

1. ✅ Tüm User Story'ler tamamlandı
2. ✅ Dokümantasyon eksiksiz
3. ✅ Test case'leri hazır
4. ✅ Uygulama çalışır durumda
5. ✅ Ek uygulamalar (4 adet) tamamlandı
6. ✅ Kod kalitesi standartlara uygun

## Değişiklik Yönetimi

Bu şartnamede yapılacak değişiklikler:
- Proje yöneticisi onayı ile
- Tüm ekip üyelerine bildirilerek
- Dokümante edilerek yapılacaktır

## İletişim

**Proje Yöneticisi:** [Hayrünnisa Koran]  
**E-posta:** [hayrunnisakoran123@gmail.com]  
**GitHub Repository:** [URL]

---

**Doküman Versiyonu:** 1.0  
**Son Güncelleme:** [Tarih]  
**Hazırlayan:** [İsim]

