"""
Kurulum Gereksinimlerini Kontrol Scripti
Bu script, veri toplama için gerekli tüm kütüphanelerin kurulu olup olmadığını kontrol eder.
"""

import sys
import os

def check_python_version():
    """Python sürümünü kontrol eder"""
    version = sys.version_info
    print(f"Python Sürümü: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        return False
    else:
        print("✓ Python sürümü uygun")
        return True

def check_package(package_name, import_name=None):
    """Belirli bir paketin kurulu olup olmadığını kontrol eder"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} kurulu")
        return True
    except ImportError:
        print(f"❌ {package_name} kurulu değil!")
        return False

def check_gemini_api_key():
    """Gemini API anahtarının ayarlanıp ayarlanmadığını kontrol eder"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    if api_key:
        print(f"✓ GEMINI_API_KEY ortam değişkeni ayarlanmış (uzunluk: {len(api_key)})")
        return True
    else:
        print("⚠ GEMINI_API_KEY ortam değişkeni ayarlanmamış")
        print("  AI metinleri üretmek için API anahtarı gereklidir")
        print("  API anahtarı almak için: https://makersuite.google.com/app/apikey")
        return False

def check_output_directory():
    """Çıktı dizininin var olup olmadığını kontrol eder"""
    output_dir = os.path.join("..", "Data", "raw")
    
    if os.path.exists(output_dir):
        print(f"✓ Çıktı dizini mevcut: {output_dir}")
        return True
    else:
        print(f"⚠ Çıktı dizini bulunamadı: {output_dir}")
        print(f"  Script çalıştırıldığında otomatik oluşturulacak")
        return True  # Bu bir hata değil, script oluşturacak

def main():
    """Ana kontrol fonksiyonu"""
    print("=" * 60)
    print("KURULUM GEREKSİNİMLERİ KONTROL EDİLİYOR")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Python sürümü kontrolü
    print("1. Python Sürümü:")
    if not check_python_version():
        all_ok = False
    print()
    
    # Gerekli paketler
    print("2. Gerekli Python Paketleri:")
    packages = [
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("arxiv", "arxiv"),
        ("google-generativeai", "google.generativeai"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("tqdm", "tqdm"),
        ("scikit-learn", "sklearn"),
        ("joblib", "joblib"),
        ("nltk", "nltk"),
    ]
    
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_ok = False
    print()
    
    # API anahtarı kontrolü
    print("3. API Anahtarı:")
    check_gemini_api_key()
    print()
    
    # Dizin kontrolü
    print("4. Dizin Yapısı:")
    check_output_directory()
    print()
    
    # Özet
    print("=" * 60)
    if all_ok:
        print("✓ Tüm temel gereksinimler karşılanıyor!")
        print("  Veri toplama scriptini çalıştırabilirsiniz:")
        print("  python data_collection.py")
    else:
        print("❌ Bazı gereksinimler eksik!")
        print("  Eksik paketleri yüklemek için:")
        print("  pip install -r requirements.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()

