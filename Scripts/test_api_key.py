"""
API Key'i test eden basit script
"""

import os
import google.generativeai as genai
import sys

# Windows terminal encoding sorunu için
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("❌ HATA: GEMINI_API_KEY ortam değişkeni ayarlanmamış!")
    print("\nAPI key'i ayarlamak için:")
    print('  $env:GEMINI_API_KEY="your-api-key"')
    sys.exit(1)

print("=" * 60)
print("API KEY TEST EDİLİYOR")
print("=" * 60)
print(f"\nAPI Key: {GEMINI_API_KEY[:20]}...{GEMINI_API_KEY[-10:]}")
print()

genai.configure(api_key=GEMINI_API_KEY)

# 1. Model listesi testi
print("1. Model listesi alınıyor...")
try:
    models = genai.list_models()
    available_models = []
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            short_name = m.name.replace('models/', '')
            available_models.append(short_name)
    print(f"   ✓ {len(available_models)} model bulundu")
    if available_models:
        print(f"   İlk 5 model: {available_models[:5]}")
except Exception as e:
    print(f"   ❌ HATA: {e}")
    sys.exit(1)

# 2. Model oluşturma testi
print("\n2. Model oluşturuluyor...")
model = None
test_models = ['gemini-2.0-flash-exp', 'gemini-2.5-flash-lite', 'gemini-1.5-flash', 'gemini-pro']

for m_name in test_models:
    try:
        model = genai.GenerativeModel(m_name)
        print(f"   ✓ Model oluşturuldu: {m_name}")
        break
    except Exception as e:
        error_msg = str(e).lower()
        is_quota = "429" in str(e) or "quota" in error_msg
        if is_quota:
            print(f"   ⚠ {m_name}: Quota hatası")
        else:
            print(f"   - {m_name}: {str(e)[:50]}")

if not model:
    print("\n❌ Hiçbir model oluşturulamadı!")
    sys.exit(1)

# 3. İlk API isteği testi
print("\n3. İlk API isteği yapılıyor...")
test_prompt = "Write a short academic abstract about photosynthesis. 100 words."
try:
    print(f"   Prompt: {test_prompt[:50]}...")
    print("   İstek gönderiliyor...")
    response = model.generate_content(test_prompt)
    
    if response and hasattr(response, 'text'):
        text = response.text.strip()
        print(f"   ✓ BAŞARILI! ({len(text)} karakter)")
        print(f"   İlk 100 karakter: {text[:100]}...")
    else:
        print("   ❌ Boş yanıt alındı!")
        sys.exit(1)
        
except Exception as e:
    error_msg = str(e).lower()
    is_quota = "429" in str(e) or "quota" in error_msg or "resource exhausted" in error_msg
    
    if is_quota:
        print(f"   ❌ QUOTA HATASI: {e}")
        print("\n📋 ÇÖZÜM:")
        print("   1. Birkaç saat bekleyin (quota reset olur)")
        print("   2. Yeni bir API key oluşturun")
        print("   3. Google Cloud Console'dan quota durumunuzu kontrol edin")
    else:
        print(f"   ❌ HATA: {e}")
    sys.exit(1)

# 4. İkinci istek testi (rate limiting kontrolü)
print("\n4. İkinci API isteği yapılıyor (rate limiting test)...")
import time
time.sleep(2)  # 2 saniye bekle
try:
    response2 = model.generate_content("Write a short abstract about quantum mechanics. 100 words.")
    if response2 and hasattr(response2, 'text'):
        print(f"   ✓ İkinci istek de başarılı! ({len(response2.text.strip())} karakter)")
    else:
        print("   ⚠ İkinci istek boş yanıt verdi")
except Exception as e:
    error_msg = str(e).lower()
    is_quota = "429" in str(e) or "quota" in error_msg
    if is_quota:
        print(f"   ⚠ İkinci istek quota hatası: {e}")
        print("   (Bu normal olabilir, rate limiting çalışıyor)")
    else:
        print(f"   ⚠ İkinci istek hatası: {e}")

print("\n" + "=" * 60)
print("✅ API KEY ÇALIŞIYOR!")
print("=" * 60)
print("\n💡 Script'i çalıştırmak için:")
print("   cd Scripts")
print("   python generate_ai_data.py")

