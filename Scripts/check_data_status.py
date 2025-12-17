"""
Veri Seti Durum Kontrol Scripti
Data/raw klasöründeki veri dosyalarını kontrol eder
"""

import pandas as pd
import os

def check_data_status():
    """Veri dosyalarının durumunu kontrol eder"""
    base_path = os.path.join("..", "Data", "raw")
    
    print("=" * 60)
    print("VERI SETI DURUM KONTROLU")
    print("=" * 60)
    print()
    
    # Human abstracts kontrolü
    human_path = os.path.join(base_path, "human_abstracts.csv")
    if os.path.exists(human_path):
        try:
            human_df = pd.read_csv(human_path)
            human_count = len(human_df)
            print(f"✅ Human abstracts dosyasi: MEVCUT")
            print(f"   Satir sayisi: {human_count}")
            print(f"   Sutunlar: {list(human_df.columns)}")
            if 'label' in human_df.columns:
                print(f"   Label kontrolu: {human_df['label'].value_counts().to_dict()}")
        except Exception as e:
            print(f"❌ Human abstracts dosyasi okunamadi: {e}")
            human_count = 0
    else:
        print(f"❌ Human abstracts dosyasi: BULUNAMADI")
        human_count = 0
    
    print()
    
    # AI abstracts kontrolü
    ai_path = os.path.join(base_path, "ai_abstracts.csv")
    if os.path.exists(ai_path):
        try:
            ai_df = pd.read_csv(ai_path)
            ai_count = len(ai_df)
            print(f"✅ AI abstracts dosyasi: MEVCUT")
            print(f"   Satir sayisi: {ai_count}")
            print(f"   Sutunlar: {list(ai_df.columns)}")
            if 'label' in ai_df.columns:
                print(f"   Label kontrolu: {ai_df['label'].value_counts().to_dict()}")
        except Exception as e:
            print(f"❌ AI abstracts dosyasi okunamadi: {e}")
            ai_count = 0
    else:
        print(f"❌ AI abstracts dosyasi: BULUNAMADI")
        ai_count = 0
    
    print()
    print("=" * 60)
    print("OZET")
    print("=" * 60)
    print(f"Human abstracts: {human_count} adet")
    print(f"AI abstracts: {ai_count} adet")
    print(f"Toplam: {human_count + ai_count} adet")
    print()
    print(f"Gereksinim: 6000 (3000 Human + 3000 AI)")
    print()
    
    # Durum kontrolü
    human_status = "✅ TAMAM" if human_count >= 3000 else f"⚠️ EKSIK ({3000 - human_count} adet eksik)"
    ai_status = "✅ TAMAM" if ai_count >= 3000 else f"⚠️ EKSIK ({3000 - ai_count} adet eksik)"
    total_status = "✅ TAMAM" if (human_count + ai_count) >= 6000 else f"⚠️ EKSIK ({6000 - (human_count + ai_count)} adet eksik)"
    
    print(f"Human durumu: {human_status}")
    print(f"AI durumu: {ai_status}")
    print(f"Toplam durumu: {total_status}")
    print()
    
    # Öneriler
    if human_count < 3000:
        print(f"⚠️ Human verileri eksik. {3000 - human_count} adet daha toplanmali.")
    if ai_count < 3000:
        print(f"⚠️ AI verileri eksik. {3000 - ai_count} adet daha toplanmali.")
        print("   Gemini API anahtari ile veri toplama scripti calistirilmali:")
        print("   $env:GEMINI_API_KEY='your-api-key'")
        print("   python data_collection.py")
    
    if human_count >= 3000 and ai_count >= 3000:
        print("✅ Veri seti gereksinimleri karsilaniyor!")
        print("   Veri temizleme scripti calistirilabilir:")
        print("   python data_cleaning.py")
    
    print("=" * 60)

if __name__ == "__main__":
    check_data_status()
