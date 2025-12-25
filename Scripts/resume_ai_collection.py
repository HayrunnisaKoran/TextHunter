"""
AI Veri Toplamayı Devam Ettirme Scripti
- Mevcut AI verilerini kontrol eder
- Eksik verileri toplar
- Yeni API anahtarı kullanımını kolaylaştırır
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

# Yolları ayarla
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "Data" / "raw"

def check_current_status():
    """Mevcut AI verilerinin durumunu kontrol eder"""
    print("=" * 60)
    print("MEVCUT DURUM KONTROLÜ")
    print("=" * 60)
    
    # 1. Checkpoint kontrolü
    checkpoint_file = DATA_DIR / "ai_abstracts_checkpoint.json"
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint_data = json.load(f)
            print(f"✓ Checkpoint dosyası: {len(checkpoint_data)} adet")
    
    # 2. ai_abstracts.json kontrolü
    ai_json = DATA_DIR / "ai_abstracts.json"
    if ai_json.exists():
        with open(ai_json, 'r', encoding='utf-8') as f:
            ai_data = json.load(f)
            print(f"✓ ai_abstracts.json: {len(ai_data)} adet")
    
    # 3. combined_dataset.csv kontrolü
    combined_csv = DATA_DIR / "combined_dataset.csv"
    if combined_csv.exists():
        df = pd.read_csv(combined_csv)
        ai_count = len(df[df['label'] == 'AI'])
        print(f"✓ combined_dataset.csv: {ai_count} adet AI verisi")
    
    # Toplam hesapla
    all_sources = []
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            all_sources.extend(json.load(f))
    elif ai_json.exists():
        with open(ai_json, 'r', encoding='utf-8') as f:
            all_sources.extend(json.load(f))
    elif combined_csv.exists():
        df = pd.read_csv(combined_csv)
        ai_data = df[df['label'] == 'AI'].to_dict('records')
        all_sources = ai_data
    
    current_count = len(all_sources) if all_sources else 0
    target = 3000
    missing = target - current_count
    
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"Mevcut AI verisi: {current_count}")
    print(f"Hedef: {target}")
    print(f"Eksik: {missing}")
    print("=" * 60)
    
    return current_count, missing

def check_api_key():
    """API anahtarını kontrol eder"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    print("\n" + "=" * 60)
    print("API ANAHTARI KONTROLÜ")
    print("=" * 60)
    
    if api_key:
        # İlk 10 ve son 4 karakteri göster (güvenlik için)
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
        print(f"✓ API anahtarı bulundu: {masked_key}")
        return True
    else:
        print("❌ API anahtarı bulunamadı!")
        print("\nAPI anahtarı ayarlamak için:")
        print("  PowerShell: $env:GEMINI_API_KEY = 'ANAHTARINIZ'")
        print("  CMD: set GEMINI_API_KEY=ANAHTARINIZ")
        print("\nYeni API anahtarı almak için:")
        print("  https://aistudio.google.com/app/apikey")
        return False

def main():
    """Ana fonksiyon"""
    print("\n" + "=" * 60)
    print("AI VERİ TOPLAMA DURUM KONTROLÜ")
    print("=" * 60 + "\n")
    
    # Durum kontrolü
    current, missing = check_current_status()
    
    # API anahtarı kontrolü
    has_api_key = check_api_key()
    
    # Öneriler
    print("\n" + "=" * 60)
    print("ÖNERİLER")
    print("=" * 60)
    
    if missing > 0:
        if has_api_key:
            print(f"\n✓ {missing} adet eksik veri toplanacak")
            print("✓ Script'i çalıştırmak için:")
            print("  cd Scripts")
            print("  python generate_ai_data.py")
            print("\n⚠ Tahmini süre:")
            print(f"  - 10 saniye/veri: ~{missing * 10 / 3600:.1f} saat")
            print(f"  - 20 saniye/veri: ~{missing * 20 / 3600:.1f} saat")
        else:
            print("\n❌ API anahtarı gerekli!")
            print("1. Yeni API anahtarı alın: https://aistudio.google.com/app/apikey")
            print("2. API anahtarını ayarlayın")
            print("3. Script'i tekrar çalıştırın")
    else:
        print("\n✓ Tüm veriler toplanmış! (3000/3000)")
        print("✓ combined_dataset.csv dosyasını kontrol edin")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

