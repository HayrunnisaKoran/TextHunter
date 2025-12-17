# Task Board - Proje Yönetimi

## Proje Yönetim Aracı

Bu proje için **GitHub Projects** kullanılmıştır. Alternatif olarak Monday.com, GitLab Task Board veya BitBucket Task Board da kullanılabilir.

## GitHub Projects Kullanımı

### Kurulum
1. GitHub repository'de "Projects" sekmesine gidin
2. "New project" butonuna tıklayın
3. "Board" template'ini seçin
4. Proje adını "TextHunter - Human or AI Detection" olarak ayarlayın

### Board Yapısı

#### Kolonlar (Columns)
1. **Backlog** - Henüz başlanmamış görevler
2. **To Do** - Yapılacaklar
3. **In Progress** - Devam eden görevler
4. **Review** - İnceleme aşamasında
5. **Done** - Tamamlanan görevler

### Görevler (Issues)

#### Epic 1: Veri Toplama ve Hazırlama
- [ ] **US-1:** Veri Seti Toplama (3000 Human + 3000 AI)
  - [ ] ArXiv API entegrasyonu
  - [ ] Gemini API entegrasyonu
  - [ ] Veri kaydetme
  - [ ] Lisans kontrolü
- [ ] **US-2:** Veri Temizleme
  - [ ] Metin temizleme fonksiyonu
  - [ ] Tokenizasyon
  - [ ] Normalizasyon
  - [ ] Tekrar kaldırma
  - [ ] Veri doğrulama

#### Epic 2: Model Eğitimi
- [ ] **US-3:** Model Eğitimi (3 farklı algoritma)
  - [ ] Naive Bayes (BoW)
  - [ ] Naive Bayes (TF-IDF)
  - [ ] Random Forest (BoW)
  - [ ] Random Forest (TF-IDF)
  - [ ] SVM (BoW)
  - [ ] SVM (TF-IDF)
  - [ ] Model kaydetme
  - [ ] Metrik hesaplama

#### Epic 3: Web Uygulaması
- [ ] **US-4:** Model Entegrasyonu
  - [ ] Python-C# entegrasyonu
  - [ ] Model yükleme servisi
  - [ ] Tahmin servisi
  - [ ] Çoklu model desteği
- [ ] **US-5:** Yüzdelik Olasılık Gösterimi
  - [ ] Tek model tahmin sayfası
  - [ ] Çoklu model karşılaştırma sayfası
  - [ ] Progress bar'lar
  - [ ] Yüzdelik gösterimi

#### Epic 4: Dokümantasyon
- [ ] Sözleşme/Yazılım Şartnamesi
- [ ] Task Board dokümantasyonu
- [ ] UI/UX Tasarım dokümantasyonu
- [ ] Test Case dokümantasyonu
- [ ] Veri toplama kılavuzu
- [ ] Kullanım kılavuzu

#### Epic 5: Test
- [ ] STD Test Case'leri (en az 5)
- [ ] White Box Testler (en az 3)
- [ ] Unit Testler
- [ ] Integration Testler

#### Epic 6: Ek Uygulamalar
- [ ] Test Bird
- [ ] Snake Game (6 test case)
- [ ] XOX Game (Socket Programming + 3 test case)
- [ ] Kalıp Bulma (3 test case)
- [ ] Labirent ve Fare (2D oyun)

#### Epic 7: Opsiyonel - Deep Learning (Ödül İçin)
- [ ] CNN modeli
- [ ] LSTM modeli
- [ ] GRU modeli
- [ ] BiLSTM modeli
- [ ] BERT modeli
- [ ] RoBERTa modeli
- [ ] CodeBERT modeli
- [ ] Hibrit yaklaşım
- [ ] Hyperparameter kayıtları
- [ ] ROC eğrisi

## Sprint Planlama

### Sprint 1: Veri Toplama (Hafta 1-2)
- Veri toplama scriptleri
- API entegrasyonları
- Veri temizleme

### Sprint 2: Model Eğitimi (Hafta 3-4)
- ML algoritmaları
- Model eğitimi
- Model kaydetme

### Sprint 3: Web Uygulaması (Hafta 5-6)
- Backend geliştirme
- Frontend geliştirme
- Model entegrasyonu

### Sprint 4: Test ve Dokümantasyon (Hafta 7-8)
- Test yazma
- Dokümantasyon
- Ek uygulamalar

### Sprint 5: Finalizasyon (Hafta 9-10)
- Son düzenlemeler
- Kalite kontrol
- Teslim hazırlığı

## Görev Atama

### Developer 1
- Veri toplama scriptleri
- Veri temizleme
- Model eğitimi (Naive Bayes, Random Forest)

### Developer 2
- Web uygulaması backend
- Model entegrasyonu
- Python-C# entegrasyonu

### Developer 3
- Web uygulaması frontend
- UI/UX tasarımı
- Test case'leri

### Developer 4 (varsa)
- Ek uygulamalar
- Dokümantasyon
- Test yazma

## İlerleme Takibi

### Haftalık Toplantılar
- Her Pazartesi: Sprint planlama
- Her Cuma: Sprint review ve retrospective

### Metrikler
- **Velocity:** Haftalık tamamlanan görev sayısı
- **Burndown Chart:** Kalan iş miktarı
- **Cumulative Flow:** Görev durumu dağılımı

## Risk Yönetimi

### Risk 1: Veri Toplama Süresi
- **Risk:** API rate limit'ler nedeniyle uzun sürebilir
- **Çözüm:** Erken başlama, batch processing

### Risk 2: Model Eğitimi Süresi
- **Risk:** Büyük veri seti nedeniyle uzun sürebilir
- **Çözüm:** Cloud computing veya daha güçlü makine

### Risk 3: Entegrasyon Sorunları
- **Risk:** Python-C# entegrasyonu sorunlu olabilir
- **Çözüm:** Erken test, alternatif çözümler

## GitHub Projects Örnek Görünümü

```
┌─────────────┬─────────────┬──────────────┬──────────┬─────────┐
│   Backlog   │   To Do     │ In Progress  │  Review  │  Done   │
├─────────────┼─────────────┼──────────────┼──────────┼─────────┤
│ US-7 (DL)   │ US-4        │ US-3         │ US-2     │ US-1    │
│ Ek-5        │ Test Cases  │ Model Train  │ Cleaning │ Data    │
│             │             │              │          │ Collect │
└─────────────┴─────────────┴──────────────┴──────────┴─────────┘
```

## Labels (Etiketler)

- `bug` - Hata
- `feature` - Özellik
- `documentation` - Dokümantasyon
- `test` - Test
- `enhancement` - İyileştirme
- `us-1` - User Story 1
- `us-2` - User Story 2
- `us-3` - User Story 3
- `us-4` - User Story 4
- `us-5` - User Story 5
- `us-7` - User Story 7 (Opsiyonel)
- `ek-1` - Ek Uygulama 1
- `ek-2` - Ek Uygulama 2
- `ek-3` - Ek Uygulama 3
- `ek-4` - Ek Uygulama 4
- `ek-5` - Ek Uygulama 5

## Milestone'lar

### Milestone 1: Veri Hazır (Hafta 2)
- ✅ 6000 örnek toplandı
- ✅ Veri temizlendi

### Milestone 2: Modeller Eğitildi (Hafta 4)
- ✅ 6 model eğitildi
- ✅ Modeller kaydedildi

### Milestone 3: Uygulama Çalışıyor (Hafta 6)
- ✅ Web uygulaması çalışıyor
- ✅ Tahminler yapılabiliyor

### Milestone 4: Test ve Dokümantasyon (Hafta 8)
- ✅ Test case'leri hazır
- ✅ Dokümantasyon tamamlandı

### Milestone 5: Teslim Hazır (Hafta 10)
- ✅ Tüm görevler tamamlandı
- ✅ Ek uygulamalar hazır
- ✅ Proje teslim edilebilir

## Notlar

- Her görev için **Definition of Done** kriterleri belirlenmelidir
- Code review zorunludur
- Test coverage minimum %70 olmalıdır
- Her commit için anlamlı commit mesajları yazılmalıdır

---

**Son Güncelleme:** [Tarih]  
**Proje Durumu:** In Progress

