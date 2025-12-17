# SonarQube / Source Monitor Analiz Kılavuzu

## Yazılım Kalitesi Analizi

Bu doküman, TextHunter projesi için kod kalitesi analiz araçlarının kullanımını açıklar.

## SonarQube Analizi

### Kurulum

#### 1. SonarQube Server Kurulumu
1. SonarQube Community Edition'ı indirin: https://www.sonarqube.org/downloads/
2. ZIP dosyasını çıkarın
3. `bin` klasöründen başlatın:
   - **Windows:** `StartSonar.bat`
   - **Linux/Mac:** `sonar.sh start`

#### 2. SonarQube Scanner Kurulumu
1. SonarScanner'ı indirin: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
2. PATH'e ekleyin

#### 3. Proje Yapılandırması

**sonar-project.properties** dosyası oluşturun:
```properties
sonar.projectKey=texthunter
sonar.projectName=TextHunter
sonar.projectVersion=1.0
sonar.sources=.
sonar.exclusions=**/bin/**,**/obj/**,**/node_modules/**,**/wwwroot/lib/**
sonar.cs.analyzer.projectOutPaths=obj
sonar.cs.analyzer.projectOutPaths=bin
```

### Analiz Çalıştırma

#### 1. Build
```bash
dotnet build
```

#### 2. SonarQube Analizi
```bash
sonar-scanner
```

#### 3. Sonuçları Görüntüleme
1. Tarayıcıda `http://localhost:9000` adresine gidin
2. Projeyi seçin
3. Analiz sonuçlarını görüntüleyin

### Analiz Metrikleri

#### Code Smells
- **Hedef:** 0 Critical, 0 Blocker
- **Kabul Edilebilir:** < 10 Major, < 50 Minor

#### Code Coverage
- **Hedef:** %80+
- **Kabul Edilebilir:** %70+

#### Duplicated Code
- **Hedef:** %0
- **Kabul Edilebilir:** < %3

#### Technical Debt
- **Hedef:** < 1 saat
- **Kabul Edilebilir:** < 5 saat

### Örnek Analiz Sonuçları

```
Project: TextHunter
Lines of Code: 2,500
Code Smells: 5 (0 Critical, 0 Blocker, 2 Major, 3 Minor)
Bugs: 0
Vulnerabilities: 0
Security Hotspots: 0
Code Coverage: 85%
Duplicated Code: 1.2%
Technical Debt: 2h 30m
Maintainability Rating: A
Reliability Rating: A
Security Rating: A
```

## Source Monitor Analizi

### Kurulum

1. Source Monitor'ü indirin: https://www.campwoodsw.com/sourcemonitor.html
2. Kurulumu tamamlayın

### Analiz Çalıştırma

#### 1. Yeni Proje Oluşturma
1. Source Monitor'ü açın
2. "File > New Project" seçin
3. Proje adını girin: "TextHunter"
4. Kaynak kod klasörünü seçin

#### 2. Analiz Ayarları
- **File Types:** *.cs
- **Exclude:** bin, obj, Tests (opsiyonel)

#### 3. Analiz Çalıştırma
1. "Project > Checkpoint" seçin
2. Checkpoint adı girin: "v1.0"
3. "OK" butonuna tıklayın

### Analiz Metrikleri

#### Complexity Metrics
- **Cyclomatic Complexity:** Ortalama < 10
- **Max Complexity:** < 20

#### Code Metrics
- **Lines of Code:** Toplam satır sayısı
- **Statements:** Toplam statement sayısı
- **Functions:** Toplam fonksiyon sayısı
- **Classes:** Toplam sınıf sayısı

#### Quality Metrics
- **Average Complexity:** < 5
- **Max Complexity:** < 15
- **File Complexity:** < 10

### Örnek Analiz Sonuçları

#### Kiviyat Grafiği (Complexity Distribution)
```
Complexity Range    | Count
-------------------|-------
1-5                | 45
6-10               | 12
11-15              | 3
16-20              | 1
21+                | 0
```

#### Block Histogram
```
Block Size Range   | Count
-------------------|-------
1-50               | 35
51-100             | 15
101-200            | 8
201-500            | 2
501+               | 1
```

## Analiz Sonuçları Yorumlama

### Code Smells (SonarQube)

#### Critical Issues
- **Örnek:** Null reference exception riski
- **Çözüm:** Null check ekleme

#### Major Issues
- **Örnek:** Unused variable
- **Çözüm:** Kullanılmayan kodları kaldırma

#### Minor Issues
- **Örnek:** Magic number
- **Çözüm:** Constant tanımlama

### Complexity Issues (Source Monitor)

#### Yüksek Complexity
- **Sorun:** Fonksiyon çok karmaşık
- **Çözüm:** Fonksiyonu bölme, refactoring

#### Yüksek Block Size
- **Sorun:** Kod bloğu çok uzun
- **Çözüm:** Fonksiyonlara bölme

## İyileştirme Önerileri

### 1. Code Duplication
- **Sorun:** Aynı kod tekrarlanıyor
- **Çözüm:** Helper methods, base classes

### 2. Long Methods
- **Sorun:** Metotlar çok uzun
- **Çözüm:** Metotları bölme, Single Responsibility

### 3. High Complexity
- **Sorun:** Cyclomatic complexity yüksek
- **Çözüm:** Conditional logic'i basitleştirme

### 4. Naming Conventions
- **Sorun:** İsimlendirme tutarsız
- **Çözüm:** C# naming conventions uygulama

## Sürekli İyileştirme

### Pre-commit Checks
- Code analysis otomatik çalıştırma
- Quality gate kontrolü

### CI/CD Integration
- Her commit'te analiz
- Quality gate failure'da build durdurma

## Raporlama

### Analiz Raporu Formatı
1. **Özet:** Genel metrikler
2. **Detaylar:** Issue listesi
3. **Grafikler:** Trend analizi
4. **Öneriler:** İyileştirme önerileri

### Rapor Örneği
```
TextHunter - Code Quality Report
Date: [Tarih]
Version: 1.0

Summary:
- Lines of Code: 2,500
- Code Smells: 5
- Code Coverage: 85%
- Technical Debt: 2h 30m
- Quality Gate: PASSED

Issues:
1. [Minor] Magic number in HomeController.cs:45
2. [Major] Unused variable in ModelPredictionService.cs:23

Recommendations:
1. Extract constants for magic numbers
2. Remove unused code
3. Increase test coverage to 90%
```

## Best Practices

### 1. Düzenli Analiz
- Her sprint sonunda analiz
- Release öncesi detaylı analiz

### 2. Quality Gates
- Minimum coverage: %70
- Maximum complexity: 15
- Zero critical issues

### 3. Team Awareness
- Analiz sonuçlarını paylaşma
- İyileştirme planları oluşturma

---

**Analiz Versiyonu:** 1.0  
**Son Güncelleme:** [Tarih]  
**Analiz Yapan:** [İsim]

