# 🚀 GitHub'a Yükleme Kılavuzu

Bu kılavuz TextHunter projesini GitHub'a yükleme adımlarını içerir.

---

## 📋 Ön Hazırlık

### 1. Git'in Kurulu Olduğunu Kontrol Et
```powershell
git --version
```

### 2. GitHub Hesabı
- [GitHub](https://github.com) hesabınız olmalı
- GitHub'da yeni bir repository oluşturun (örn: `TextHunter`)

---

## 📁 Veri Dosyaları Hakkında Önemli Bilgi

### Mevcut Veri Boyutları
| Dosya | Boyut |
|-------|-------|
| combined_dataset.csv | ~10.3 MB |
| combined_dataset.json | ~11.2 MB |
| human_abstracts.csv | ~4.6 MB |
| human_abstracts.json | ~5.3 MB |
| ai_abstracts.csv | ~5.6 MB |
| ai_abstracts.json | ~6.0 MB |
| **Toplam** | **~43 MB** |

### Seçenekler

**Seçenek 1: Veri dosyalarını dahil et (Önerilen - Küçük projeler için)**
- Tüm dosyaları olduğu gibi yükle
- GitHub 100 MB'a kadar tek dosya kabul eder

**Seçenek 2: Veri dosyalarını hariç tut**
- `.gitignore`'da veri dosyalarını yorumdan çıkar
- Sadece kod ve dokümantasyon yükle
- Veri setini ayrı paylaş (Google Drive, OneDrive vb.)

**Seçenek 3: Git LFS kullan (Büyük dosyalar için)**
```powershell
# Git LFS kurulumu
git lfs install
git lfs track "*.csv"
git lfs track "*.json"
```

---

## 🔧 Adım Adım GitHub'a Yükleme

### Adım 1: Git Repo Başlat
```powershell
cd C:\PROJELER\TextHunter_Klasörü\TextHunter
git init
```

### Adım 2: Git Kullanıcı Bilgilerini Ayarla (İlk kez yapılır)
```powershell
git config user.name "Adınız Soyadınız"
git config user.email "email@example.com"
```

### Adım 3: .gitignore Kontrol Et
Proje klasöründe `.gitignore` dosyası mevcut. İçeriğini kontrol edin.

### Adım 4: Dosyaları Ekle
```powershell
# Tüm dosyaları stage'e ekle
git add .

# Durumu kontrol et
git status
```

### Adım 5: İlk Commit
```powershell
git commit -m "Initial commit: TextHunter - Human or AI Text Detection"
```

### Adım 6: GitHub Remote Ekle
```powershell
# GitHub'da oluşturduğunuz repo URL'sini kullanın
git remote add origin https://github.com/KULLANICI_ADI/TextHunter.git
```

### Adım 7: GitHub'a Push
```powershell
# İlk push (main branch)
git branch -M main
git push -u origin main
```

---

## 📝 Örnek Tam Komut Dizisi

```powershell
# Proje klasörüne git
cd C:\PROJELER\TextHunter_Klasörü\TextHunter

# Git başlat
git init

# Kullanıcı bilgileri (kendi bilgilerinizi girin)
git config user.name "Kullanici Adi"
git config user.email "email@ornek.com"

# Dosyaları ekle
git add .

# Commit
git commit -m "Initial commit: TextHunter Project"

# Remote ekle (kendi repo URL'nizi kullanın)
git remote add origin https://github.com/USERNAME/TextHunter.git

# Push
git branch -M main
git push -u origin main
```

---

## ⚠️ Yaygın Hatalar ve Çözümleri

### Hata 1: "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/USERNAME/TextHunter.git
```

### Hata 2: "error: failed to push some refs"
```powershell
git pull origin main --rebase
git push -u origin main
```

### Hata 3: "File too large" (100 MB üzeri dosya)
```powershell
# Büyük dosyayı .gitignore'a ekle veya Git LFS kullan
git lfs install
git lfs track "*.pkl"  # Örnek: model dosyaları
```

### Hata 4: Authentication Failed
GitHub artık şifre ile giriş desteklemiyor. Personal Access Token kullanın:
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" → repo yetkisi ver
3. Token'ı şifre yerine kullan

---

## 🔄 Sonraki Push'lar

```powershell
# Değişiklikleri ekle
git add .

# Commit
git commit -m "Commit mesajı"

# Push
git push
```

---

## 📋 Kontrol Listesi

- [ ] Git kurulu mu?
- [ ] GitHub hesabı var mı?
- [ ] GitHub'da yeni repo oluşturuldu mu?
- [ ] `.gitignore` kontrol edildi mi?
- [ ] Veri dosyaları dahil mi / hariç mi karar verildi mi?
- [ ] `git init` yapıldı mı?
- [ ] İlk commit yapıldı mı?
- [ ] Remote eklendi mi?
- [ ] Push başarılı mı?

---

## 📞 Yardım

Sorun yaşarsanız:
- [Git Dokümantasyonu](https://git-scm.com/doc)
- [GitHub Yardım](https://docs.github.com)

---

**Son Güncelleme:** 17 Aralık 2025

