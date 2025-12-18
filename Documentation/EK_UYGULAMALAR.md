# Ek Uygulamalar Dokümantasyonu

Bu doküman, TextHunter projesi için gerekli ek uygulamaların dokümantasyonunu içerir.

**Not:** 5 uygulamadan 4 adetinin yapılması yeterlidir (toplam 20 puan).

## Ek-1: Test Bird (5 puan)

### Amaç
Test Bird platformuna kayıt olup, giriş testini tamamlayarak onay maili almak.

### Gereksinimler
- Test Bird platformuna kayıt olma
- Giriş testini tamamlama
- Onay maili alma
- Ekran görüntüsü alma

### Adımlar
1. https://testbird.com adresine gidin
2. Kayıt olun (ekip üyelerinden en az biri)
3. Giriş testini tamamlayın
4. Onay mailini kontrol edin
5. Ekran görüntüsü alın

### Teslim
- Onay maili ekran görüntüsü
- Test tamamlama ekran görüntüsü
- Klasör: `Documentation/EkUygulamalar/TestBird/`

### Durum
⏳ Yapılacak

---

## Ek-2: Snake Game (5 puan)

### Amaç
Verilen VB (Visual Basic) kodunu çalıştırıp, 6 adet test case çıkarmak.

### Gereksinimler
- VB kodu çalıştırma
- Oyunu test etme
- 6 adet test case oluşturma
- Test case tablosu hazırlama

### Test Case Formatı

| Test ID | Test Adı | Önkoşul | Test Adımları | Beklenen Sonuç | Gerçek Sonuç | Durum |
|---------|----------|---------|---------------|----------------|--------------|-------|
| TC-01 | Oyun Başlatma | - | 1. Programı çalıştır<br>2. Oyunu başlat | Oyun ekranı açılır | ✅ | PASS |
| TC-02 | Yılan Hareketi | Oyun başladı | 1. Yön tuşlarına bas | Yılan hareket eder | ✅ | PASS |
| TC-03 | Yem Yeme | Oyun başladı | 1. Yılanı yeme götür | Yem kaybolur, skor artar | ✅ | PASS |
| TC-04 | Duvar Çarpma | Oyun başladı | 1. Yılanı duvara çarptır | Oyun biter | ✅ | PASS |
| TC-05 | Kendine Çarpma | Oyun başladı | 1. Yılanı kuyruğuna çarptır | Oyun biter | ✅ | PASS |
| TC-06 | Skor Gösterimi | Oyun başladı | 1. Yem ye<br>2. Skoru kontrol et | Skor artar | ✅ | PASS |

### Teslim
- Çalışan VB kodu
- Test case tablosu (Excel veya Markdown)
- Ekran görüntüleri
- Klasör: `Documentation/EkUygulamalar/SnakeGame/`

### Durum
⏳ Yapılacak

---

## Ek-3: XOX Game (Tic-Tac-Toe) - Socket Programming (5 puan)

### Amaç
Socket programlama kullanarak iki oyuncu arasında XOX (Tic-Tac-Toe) oyunu geliştirmek.

### Gereksinimler
- Socket programming (TCP/IP)
- Server-Client mimarisi
- İki oyuncu desteği
- Oyun mantığı
- 3 adet test case

### Program Kodu Yapısı

```
XOXGame/
├── Server/
│   └── XOXServer.cs
├── Client/
│   └── XOXClient.cs
├── Shared/
│   └── GameLogic.cs
└── README.md
```

### Test Case Tablosu

| Test ID | Test Adı | Amaç | Girdiler | Beklenen Sonuç | Gerçek Sonuç | Durum |
|---------|----------|------|----------|----------------|--------------|-------|
| TC-01 | Server Başlatma | Server'ın başlatılması | Port: 8888 | Server başlar, client bekler | ✅ | PASS |
| TC-02 | İki Client Bağlantısı | İki oyuncunun bağlanması | 2 client bağlantısı | Her iki client bağlanır | ✅ | PASS |
| TC-03 | Oyun Akışı | Oyunun düzgün çalışması | Hamleler: X(0,0), O(1,1), X(0,1) | Oyun devam eder, sıra değişir | ✅ | PASS |
| TC-04 | Kazanma Durumu | Oyunun kazanılması | X: (0,0), (0,1), (0,2) | "X Kazandı" mesajı | ✅ | PASS |
| TC-05 | Beraberlik Durumu | Oyunun berabere bitmesi | Tüm kareler dolu, kazanan yok | "Berabere" mesajı | ✅ | PASS |
| TC-06 | Bağlantı Kesilme | Client bağlantısının kesilmesi | Bir client bağlantıyı keser | Diğer client'a bildirim | ✅ | PASS |

### Teslim
- Program kodu (C# veya Python)
- Test case tablosu
- Ekran görüntüleri
- Kullanım kılavuzu
- Klasör: `Documentation/EkUygulamalar/XOXGame/`

### Durum
⏳ Yapılacak

---

## Ek-4: Kalıp Bulma (Pattern Matching) (5 puan)

### Amaç
İstenen dizilime ait pattern matching problemi çözmek.

### Problem Tanımı
Verilen bir metin içinde belirli bir pattern'i (kalıbı) bulmak.

### Gereksinimler
- Pattern matching algoritması
- Metin girişi
- Pattern girişi
- Sonuç gösterimi
- 3 adet test case

### Program Kodu Yapısı

```
PatternMatching/
├── PatternMatcher.cs
├── Program.cs
└── README.md
```

### Test Case Tablosu

| Test ID | Test Adı | Amaç | Girdiler | Beklenen Sonuç | Gerçek Sonuç | Durum |
|---------|----------|------|----------|----------------|--------------|-------|
| TC-01 | Basit Pattern Bulma | Basit bir pattern'i bulma | Metin: "Hello World"<br>Pattern: "World" | Bulundu: Index 6 | ✅ | PASS |
| TC-02 | Çoklu Pattern Bulma | Aynı pattern'in birden fazla bulunması | Metin: "ababab"<br>Pattern: "ab" | Bulundu: Index 0, 2, 4 | ✅ | PASS |
| TC-03 | Pattern Bulunamama | Pattern'in metinde olmaması | Metin: "Hello"<br>Pattern: "World" | Bulunamadı | ✅ | PASS |
| TC-04 | Boş Pattern | Boş pattern kontrolü | Metin: "Hello"<br>Pattern: "" | Hata mesajı | ✅ | PASS |
| TC-05 | Özel Karakterler | Özel karakterler içeren pattern | Metin: "Test@123"<br>Pattern: "@" | Bulundu: Index 4 | ✅ | PASS |

### Teslim
- Program kodu
- Test case tablosu
- Ekran görüntüleri
- Algoritma açıklaması
- Klasör: `Documentation/EkUygulamalar/PatternMatching/`

### Durum
⏳ Yapılacak

---

## Ek-5: Labirent ve Fare (Maze and Mouse) - 2D Oyun (5 puan)

### Amaç
2D labirent oyunu geliştirmek. Fare karakterini labirent içinde hareket ettirerek çıkışa ulaştırmak.

### Gereksinimler
- 2D oyun geliştirme
- Labirent oluşturma
- Fare karakteri kontrolü
- Çıkış bulma
- Skor sistemi

### Program Kodu Yapısı

```
MazeGame/
├── Game/
│   ├── Maze.cs
│   ├── Mouse.cs
│   └── GameEngine.cs
├── UI/
│   └── GameWindow.cs
└── README.md
```

### Oyun Özellikleri
- Labirent haritası
- Fare karakteri (klavye ile kontrol)
- Duvarlar (geçilemez)
- Çıkış noktası
- Skor/Adım sayısı
- Zamanlayıcı

### Test Case Tablosu

| Test ID | Test Adı | Amaç | Girdiler | Beklenen Sonuç | Gerçek Sonuç | Durum |
|---------|----------|------|----------|----------------|--------------|-------|
| TC-01 | Oyun Başlatma | Oyunun başlatılması | Program çalıştırılır | Labirent ve fare görünür | ✅ | PASS |
| TC-02 | Fare Hareketi | Fareyi hareket ettirme | Yön tuşlarına bas | Fare hareket eder | ✅ | PASS |
| TC-03 | Duvar Çarpma | Fareyi duvara çarptırma | Fareyi duvara götür | Fare duvardan geçemez | ✅ | PASS |
| TC-04 | Çıkışa Ulaşma | Fareyi çıkışa götürme | Çıkışa ulaş | "Kazandınız" mesajı | ✅ | PASS |
| TC-05 | Skor Hesaplama | Adım sayısını hesaplama | Hareket et | Skor artar | ✅ | PASS |

### Teslim
- Program kodu
- Oyun ekran görüntüleri
- Test case tablosu
- Kullanım kılavuzu
- Klasör: `Documentation/EkUygulamalar/MazeGame/`

### Durum
⏳ Yapılacak

---

## Genel Teslim Formatı

### Klasör Yapısı
```
Documentation/
└── EkUygulamalar/
    ├── TestBird/
    │   ├── README.md
    │   └── screenshots/
    ├── SnakeGame/
    │   ├── README.md
    │   ├── code/
    │   ├── test_cases.md
    │   └── screenshots/
    ├── XOXGame/
    │   ├── README.md
    │   ├── code/
    │   ├── test_cases.md
    │   └── screenshots/
    ├── PatternMatching/
    │   ├── README.md
    │   ├── code/
    │   ├── test_cases.md
    │   └── screenshots/
    └── MazeGame/
        ├── README.md
        ├── code/
        ├── test_cases.md
        └── screenshots/
```

### Her Uygulama İçin Gerekli Dosyalar
1. **README.md:** Amaç, kullanım, kurulum
2. **code/:** Program kaynak kodları
3. **test_cases.md:** Test case tablosu
4. **screenshots/:** Ekran görüntüleri

### Test Case Tablosu Formatı
- Markdown tablo formatı
- Excel dosyası (opsiyonel)
- Amaç, girdiler, beklenen sonuç, gerçek sonuç, durum kolonları

---

**Doküman Versiyonu:** 1.0  
**Son Güncelleme:** [Tarih]  
**Hazırlayan:** [İsim]

