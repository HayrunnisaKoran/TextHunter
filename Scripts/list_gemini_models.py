"""
Gemini API'de mevcut modelleri listeleyen script
"""

import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("❌ HATA: GEMINI_API_KEY ortam değişkeni ayarlanmamış!")
    exit(1)

print("=" * 60)
print("GEMINI API MODELLERİ LİSTELENİYOR")
print("=" * 60)
print()

genai.configure(api_key=GEMINI_API_KEY)

try:
    # Mevcut modelleri listele
    print("Mevcut modeller listeleniyor...\n")
    models = genai.list_models()
    
    available_models = []
    for model in models:
        # Sadece generateContent destekleyen modelleri göster
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"✓ {model.name}")
            print(f"  Desteklenen metodlar: {', '.join(model.supported_generation_methods)}")
            print()
    
    if available_models:
        print("=" * 60)
        print("KULLANILABİLİR MODELLER:")
        print("=" * 60)
        for model_name in available_models:
            # Model ismini kısa hale getir (models/ öneki olmadan)
            short_name = model_name.replace('models/', '')
            print(f"  - {short_name}")
        
        print("\n" + "=" * 60)
        print("ÖNERİLEN MODEL:")
        print("=" * 60)
        # En uygun modeli seç
        if any('gemini-1.5-pro' in m for m in available_models):
            recommended = [m for m in available_models if 'gemini-1.5-pro' in m][0]
        elif any('gemini-1.5-flash' in m for m in available_models):
            recommended = [m for m in available_models if 'gemini-1.5-flash' in m][0]
        elif any('gemini-pro' in m for m in available_models):
            recommended = [m for m in available_models if 'gemini-pro' in m][0]
        else:
            recommended = available_models[0] if available_models else None
        
        if recommended:
            short_name = recommended.replace('models/', '')
            print(f"  {short_name}")
            print(f"\nBu modeli kullanmak için scriptte şu satırı kullanın:")
            print(f"  model = genai.GenerativeModel('{short_name}')")
    else:
        print("❌ Hiçbir model bulunamadı!")
        
except Exception as e:
    print(f"❌ HATA: {e}")
    print("\nAlternatif çözüm: Model ismini manuel olarak deneyin:")
    print("  - gemini-pro")
    print("  - gemini-1.5-pro")
    print("  - gemini-1.5-flash")

