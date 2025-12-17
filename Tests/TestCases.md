# Test Case Dökümanı

## Test Case 1: Text Classification - Başarılı Tahmin
**Test ID:** TC-001  
**Test Adı:** Text Classification - Başarılı Tahmin  
**Önkoşul:** Uygulama çalışıyor, modeller eğitilmiş  
**Test Adımları:**
1. Tarayıcıda uygulamayı aç
2. "Text Classification" sayfasına git
3. Metin alanına örnek bir metin gir: "This is a research paper about machine learning algorithms and their applications in natural language processing."
4. Model dropdown'ından "naive_bayes_bow" seç
5. "Submit" butonuna tıkla
**Beklenen Sonuç:** 
- Sayfa yüklenir
- Tahmin sonucu gösterilir (Human veya AI)
- Yüzdelik olasılıklar gösterilir (Human % ve AI %)
- Progress bar'lar doğru yüzdeleri gösterir

---

## Test Case 2: Text Classification - Boş Metin Kontrolü
**Test ID:** TC-002  
**Test Adı:** Text Classification - Boş Metin Validasyonu  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. "Text Classification" sayfasına git
2. Metin alanını boş bırak
3. Bir model seç
4. "Submit" butonuna tıkla
**Beklenen Sonuç:** 
- Hata mesajı gösterilir: "Lütfen bir metin girin."
- Sayfa yeniden yüklenir
- Tahmin sonucu gösterilmez

---

## Test Case 3: Model Comparison - Çoklu Model Tahmini
**Test ID:** TC-003  
**Test Adı:** Model Comparison - Tüm Modellerin Tahmin Sonuçları  
**Önkoşul:** Uygulama çalışıyor, modeller eğitilmiş  
**Test Adımları:**
1. "Model Comparison" sayfasına git
2. Metin alanına örnek bir metin gir: "Deep learning models have revolutionized the field of artificial intelligence."
3. "Submit" butonuna tıkla
**Beklenen Sonuç:** 
- Tüm modellerin tahmin sonuçları tabloda gösterilir
- Her model için Human % ve AI % yüzdeleri gösterilir
- En az 3 farklı model sonucu görünür
- Tablo düzgün formatlanmıştır

---

## Test Case 4: Clear Butonu Fonksiyonelliği
**Test ID:** TC-004  
**Test Adı:** Clear Butonu - Metin Temizleme  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. "Text Classification" veya "Model Comparison" sayfasına git
2. Metin alanına bir metin gir
3. "Clear" butonuna tıkla
**Beklenen Sonuç:** 
- Metin alanı temizlenir
- Önceki tahmin sonuçları (varsa) kaybolur veya gizlenir

---

## Test Case 5: Model Dropdown - Model Seçimi
**Test ID:** TC-005  
**Test Adı:** Text Classification - Model Seçimi  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. "Text Classification" sayfasına git
2. Model dropdown'ını aç
3. Farklı modelleri seç (naive_bayes_bow, random_forest_tfidf, svm_bow)
4. Her seçimde bir metin gir ve submit et
**Beklenen Sonuç:** 
- Dropdown'da en az 6 farklı model seçeneği görünür
- Her model seçildiğinde tahmin yapılabilir
- Farklı modeller farklı sonuçlar verebilir

---

## Test Case 6: Navigation - Sayfa Geçişleri
**Test ID:** TC-006  
**Test Adı:** Navigation Menüsü - Sayfa Geçişleri  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. Ana sayfadan "Text Classification" linkine tıkla
2. "Model Comparison" linkine tıkla
3. Her iki sayfa arasında geçiş yap
**Beklenen Sonuç:** 
- Tüm sayfalar düzgün yüklenir
- Navigation menüsü her sayfada görünür
- Sayfa geçişleri sorunsuz çalışır

---

## Test Case 7: Responsive Tasarım - Mobil Görünüm
**Test ID:** TC-007  
**Test Adı:** Responsive Tasarım Kontrolü  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. Tarayıcıyı mobil görünüme al (responsive mode)
2. Tüm sayfaları kontrol et
**Beklenen Sonuç:** 
- Sayfalar mobil görünümde düzgün görünür
- Metin alanları ve butonlar erişilebilir
- Tablolar ve progress bar'lar düzgün görünür

---

## Test Case 8: Hata Yönetimi - Model Bulunamadı
**Test ID:** TC-008  
**Test Adı:** Model Dosyası Bulunamadığında Hata Yönetimi  
**Önkoşul:** Uygulama çalışıyor, model dosyaları silinmiş  
**Test Adımları:**
1. MLModels klasöründeki model dosyalarını geçici olarak başka yere taşı
2. Uygulamada tahmin yapmayı dene
**Beklenen Sonuç:** 
- Kullanıcıya anlaşılır bir hata mesajı gösterilir
- Uygulama çökmez
- Hata loglanır

---

## Test Case 9: Performans - Uzun Metin İşleme
**Test ID:** TC-009  
**Test Adı:** Uzun Metin İşleme Performansı  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. 5000 karakterlik uzun bir metin gir
2. Tahmin yap
**Beklenen Sonuç:** 
- Metin işlenir (kabul edilebilir sürede, max 30 saniye)
- Sonuç döner
- Uygulama donmaz

---

## Test Case 10: Özel Karakterler - Unicode Desteği
**Test ID:** TC-010  
**Test Adı:** Özel Karakter ve Unicode Desteği  
**Önkoşul:** Uygulama çalışıyor  
**Test Adımları:**
1. Türkçe karakterler içeren metin gir: "Bu bir makale özetidir. Şişli'de araştırma yapıldı."
2. Tahmin yap
**Beklenen Sonuç:** 
- Türkçe karakterler düzgün görünür
- Metin işlenir
- Sonuç döner

