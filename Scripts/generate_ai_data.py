"""
Sadece AI Verilerini Üretme Scripti (Optimize Edilmiş Versiyon)
- Mevcut human_abstracts.json dosyasını okur
- Gemini AI ile 3000 AI yazımı metin üretir
- Stabilite için worker sayısı düşürüldü ve bekleme süreleri optimize edildi
"""

import os
import json
import time
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import google.generativeai as genai
from typing import List, Dict
import threading
import random
import sys
import signal

# Windows terminal encoding sorunu için
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Özel Exception sınıfı
class QuotaExceededException(Exception):
    """API quota limiti aşıldığında fırlatılır"""
    pass

# --- YAPILANDIRMA (KRİTİK AYARLAR) ---
# VAR OLAN HESAPLAR İÇİN: Günlük quota tükenmiş olabilir
# Bu yüzden günlük küçük batch'ler halinde çekmek daha iyi
AI_COUNT = 1000  # Mevcut AI verilerinin üzerine 1000 ek veri çekilecek
# Günlük batch için: Her gün 50-100 veri çekmek daha güvenli
# Ortam değişkeninden ayarlanabilir: $env:DAILY_BATCH_SIZE=50
DAILY_BATCH_SIZE = int(os.getenv("DAILY_BATCH_SIZE", "50"))  # Günlük çekilecek veri sayısı
OUTPUT_DIR = "../Data/raw"
INPUT_FILE = os.path.join(OUTPUT_DIR, "human_abstracts.json")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "ai_abstracts_checkpoint.json")
DIVERSE_PROMPTS_FILE = os.path.join(OUTPUT_DIR, "diverse_prompts.csv")  # Çeşitli promptlar

# OPTİMİZASYON AYARLARI
# Hızlı veri toplama için optimize edilmiş
MAX_WORKERS = 1  # 1 thread - quota korunması için (güvenli)
# Not: 2 worker yaparsanız daha hızlı olur ama quota 2x hızla tükenir
CHECKPOINT_INTERVAL = 10 # Veri kaybını önlemek için daha sık kayıt

# HIZ AYARLARI (Optimize edilmiş - daha hızlı veri toplama)
# Gemini API limitleri: ~15 istek/dakika (ücretsiz), ~60 istek/dakika (ücretli)
# HIZLI VERİ TOPLAMA İÇİN: Daha agresif ama güvenli ayar
# - 12 saniye = 5 istek/dakika (güvenli - önerilen)
# - 10 saniye = 6 istek/dakika (orta risk - hızlı)
# - 8 saniye = 7.5 istek/dakika (daha hızlı ama riskli)
# 50 veri için: 10 saniye = ~8.3 dakika, 12 saniye = ~10 dakika
MIN_REQUEST_INTERVAL = 12.0  # 12 saniye (5 istek/dakika - hızlı ama güvenli)
# Not: Script otomatik olarak quota hatası durumunda 5 dakika bekleyip tekrar deneyecek
# Eğer quota hatası alırsanız, bu değeri 15.0 veya 20.0 yapabilirsiniz 

def load_human_abstracts() -> List[Dict]:
    if not os.path.exists(INPUT_FILE):
        print(f"⚠ UYARI: {INPUT_FILE} dosyası bulunamadı!")
        return []
    
    print(f"Mevcut human verileri yükleniyor: {INPUT_FILE}")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        human_data = json.load(f)
    print(f"✓ {len(human_data)} adet human verisi yüklendi")
    return human_data

def load_diverse_prompts() -> List[str]:
    """
    Çeşitli konulardan promptları yükler.
    Eğer diverse_prompts.csv yoksa, eski AI/ML promptlarını kullanır.
    """
    if os.path.exists(DIVERSE_PROMPTS_FILE):
        try:
            df = pd.read_csv(DIVERSE_PROMPTS_FILE)
            prompts = df['prompt'].tolist()
            print(f"✓ {len(prompts)} adet çeşitli prompt yüklendi (diverse_prompts.csv'den)")
            print(f"  Konu dağılımı: {df['category'].value_counts().to_dict()}")
            return prompts
        except Exception as e:
            print(f"⚠ diverse_prompts.csv yüklenirken hata: {e}")
            print("  Eski AI/ML promptları kullanılacak.")
    
    # Fallback: Eski AI/ML promptları
    print("⚠ diverse_prompts.csv bulunamadı, eski promptlar kullanılıyor.")
    print("  Önce create_diverse_prompts.py scriptini çalıştırın!")
    return [
        "Write a detailed academic abstract about machine learning applications in natural language processing. 150-300 words.",
        "Write a comprehensive academic abstract about deep learning models for computer vision. 150-300 words.",
        "Write an academic abstract about statistical methods in data science. 150-300 words.",
        "Write a detailed academic abstract about neural network architectures for time series. 150-300 words.",
        "Write a comprehensive academic abstract about reinforcement learning algorithms. 150-300 words.",
        "Write an academic abstract about transformer models and LLMs. 150-300 words.",
        "Write a detailed academic abstract about unsupervised learning clustering. 150-300 words."
    ]

def generate_single_ai_text(model, prompt: str, lock: threading.Lock, last_request_time: List[float], 
                            min_interval: float) -> Dict | None:
    """
    Tek bir AI metni üretir. Hata durumunda üstel bekleme (Exponential Backoff) uygular.
    """
    max_retries = 5
    base_wait_time = 5 # İlk hata beklemesi 5 saniye
    
    for attempt in range(max_retries):
        try:
            # --- Rate Limiting (Hız Kontrolü) ---
            with lock:
                current_time = time.time()
                time_since_last = current_time - last_request_time[0]
                
                # İlk istek için özel kontrol (last_request_time[0] == 0.0 ise)
                if last_request_time[0] == 0.0:
                    # İlk istek - direkt yap, bekleme yok
                    last_request_time[0] = current_time
                    print(f"\n[DEBUG] İlk API isteği yapılıyor (bekleme yok)...")
                elif time_since_last < min_interval:
                    # Sonraki istekler için bekleme
                    sleep_needed = min_interval - time_since_last
                    if sleep_needed > 0:
                        print(f"[DEBUG] Rate limiting: {sleep_needed:.1f} saniye bekleniyor...")
                        time.sleep(sleep_needed)
                    last_request_time[0] = time.time()
                else:
                    # Yeterince zaman geçti, direkt yap
                    last_request_time[0] = current_time

            # API çağrısı - Basit yaklaşım (timeout olmadan, hata yakalama ile)
            print(f"[DEBUG] API isteği gönderiliyor (deneme {attempt + 1}/{max_retries})...")
            print(f"[DEBUG] Prompt uzunluğu: {len(prompt)} karakter")
            
            # API çağrısı - direkt yap, exception handling zaten var
            response = model.generate_content(prompt)
            
            print(f"[DEBUG] API yanıtı alındı! Response tipi: {type(response)}")
            
            if not response or not hasattr(response, 'text'):
                raise ValueError("Boş yanıt")
            
            generated_text = response.text.strip()
            
            # Basit kalite kontrolü
            if len(generated_text) < 50:
                raise ValueError("Çok kısa metin")

            # DEBUG: Başarılı istek
            if attempt == 0:
                print(f"[DEBUG] İlk istek başarılı! ({len(generated_text)} karakter)")

            return {
                "text": generated_text,
                "label": "AI",
                "source": "gemini",
                "prompt": prompt,
                "generated_date": datetime.now().isoformat()
            }

        except Exception as e:
            error_msg = str(e).lower()
            full_error = str(e)
            
            # 429 veya Quota hatası tespiti
            is_rate_limit = "429" in error_msg or "quota" in error_msg or "resource exhausted" in error_msg
            
            # DEBUG: İlk istek hatası
            if attempt == 0:
                print(f"\n[DEBUG] İlk istek hatası: {full_error[:100]}")
            
            if attempt < max_retries - 1:
                if is_rate_limit:
                    # Quota hatası - çok uzun bekleyip tekrar dene (2 gün içinde bitirmek için)
                    # Belki quota reset olmuştur veya geçici bir sorundur
                    wait_time = 300 + (attempt * 60)  # 5 dakika + her denemede 1 dakika daha
                    print(f"\n⚠ Quota hatası - {int(wait_time/60)} dakika bekleniyor (quota reset olabilir)...")
                    print(f"   [DEBUG] Deneme {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue  # Tekrar dene, exception fırlatma
                else:
                    # Diğer hatalar için daha kısa bekleme
                    wait_time = (base_wait_time * (2 ** attempt)) + random.uniform(0, 2)
                    wait_time = min(wait_time, 30)  # Max 30 saniye
                    print(f"\n⚠ Hata: {full_error[:50]}... - {int(wait_time)}sn bekleniyor.")
                    print(f"   [DEBUG] Deneme {attempt + 1}/{max_retries}")
                
                time.sleep(wait_time)
                continue
            
            # Tüm denemeler başarısız
            print(f"\n[DEBUG] Tüm denemeler başarısız oldu. Son hata: {full_error[:100]}")
            return None # Tüm denemeler başarısız
    return None

def generate_ai_texts(count: int = 3000, api_key: str = "", max_workers: int = 2) -> List[Dict]:
    if not api_key:
        print("❌ HATA: GEMINI_API_KEY eksik!")
        print("\n📋 API Key'i ayarlamak için:")
        print("   PowerShell: $env:GEMINI_API_KEY = 'ANAHTARINIZ'")
        print("   CMD: set GEMINI_API_KEY=ANAHTARINIZ")
        print("\n💡 Yeni API key almak için:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n⚠ Script API key olmadan çalışamaz!")
        return []
    
    print(f"\n{'='*60}")
    print(f"Gemini AI ile {count} metin üretiliyor (STABIL MOD)")
    print(f"{'='*60}\n")
    
    genai.configure(api_key=api_key)
    
    # Önce API'den mevcut modelleri al
    available_models = []
    print("Mevcut modeller kontrol ediliyor...")
    try:
        models = genai.list_models()
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                short_name = m.name.replace('models/', '')
                available_models.append(short_name)
        if available_models:
            print(f"✓ {len(available_models)} model bulundu")
    except Exception as e:
        print(f"⚠ Model listesi alınamadı: {str(e)[:100]}")
    
    # Öncelik sıralaması - Eski modelleri önce dene (daha az quota kullanabilir)
    # 2 gün içinde bitirmek için daha stabil modelleri tercih ediyoruz
    priority_models = [
        'gemini-1.5-flash',       # Eski ama stabil, daha az quota kullanabilir
        'gemini-1.5-pro',         # Eski Pro, stabil
        'gemini-2.0-flash',       # 2.0 Flash
        'gemini-2.5-flash',       # En yeni ve hızlı (daha fazla quota kullanabilir)
        'gemini-2.0-pro',         # 2.0 Pro
        'gemini-2.5-pro',         # En yeni Pro
        'gemini-pro-latest',      # Latest versiyon
        'gemini-pro'              # Genel
    ]
    
    # Önce mevcut modellerden öncelikli olanları bul
    model_to_try = []
    if available_models:
        # Öncelik sırasına göre mevcut modellerden seç
        for preferred in priority_models:
            matching = [m for m in available_models if preferred in m.lower()]
            if matching:
                model_to_try.extend(matching)
        # Eğer hiçbiri bulunamadıysa, flash içeren modelleri, sonra diğerlerini ekle
        if not model_to_try:
            flash_models = [m for m in available_models if 'flash' in m.lower()]
            if flash_models:
                model_to_try.extend(flash_models)
            else:
                model_to_try.extend(available_models[:3])  # İlk 3 modeli dene
    else:
        # API'den liste alınamadıysa, öncelik listesini kullan
        model_to_try = priority_models
    
    model = None
    selected_model_name = ""
    
    print("Uygun model aranıyor...")
    print("NOT: Test isteği yapılmıyor (quota korunması için), direkt kullanılacak model seçiliyor...")
    
    # Quota hatası durumunda bekleyip tekrar deneme
    max_model_selection_retries = 3
    retry_wait = 300  # 5 dakika
    
    for retry_attempt in range(max_model_selection_retries):
        quota_error_count = 0
        
        for m_name in model_to_try:
            try:
                # Test isteği YAPMIYORUZ - direkt model oluşturuyoruz
                # İlk gerçek istek generate_single_ai_text içinde yapılacak
                temp_model = genai.GenerativeModel(m_name)
                model = temp_model
                selected_model_name = m_name
                print(f"✓ Model seçildi: {selected_model_name} (test isteği yapılmadı, quota korundu)")
                break
            except Exception as e:
                error_msg = str(e).lower()
                is_quota_error = "429" in str(e) or "quota" in error_msg or "resource exhausted" in error_msg
                
                if is_quota_error:
                    quota_error_count += 1
                    print(f"  - {m_name} quota hatası ({str(e)[:50]}...)")
                else:
                    print(f"  - {m_name} kullanılamadı ({str(e)[:50]}...)")
                continue
        
        # Eğer model seçildiyse, döngüden çık
        if model:
            break
        
        # Eğer tüm modeller quota hatası veriyorsa, bekleyip tekrar dene
        if quota_error_count > 0 and retry_attempt < max_model_selection_retries - 1:
            print(f"\n⚠ Tüm modeller quota hatası veriyor. {int(retry_wait/60)} dakika bekleniyor...")
            print(f"   (Deneme {retry_attempt + 1}/{max_model_selection_retries})")
            time.sleep(retry_wait)
            retry_wait *= 2  # Her denemede bekleme süresini 2x artır
            continue
            
    if not model:
        print("\n❌ Hiçbir model seçilemedi. API Key veya Kotanızı kontrol edin.")
        print("\n📋 ÇÖZÜM ÖNERİLERİ:")
        print("   1. Birkaç saat bekleyin (quota genelde saatlik/günlük reset olur)")
        print("   2. Google Cloud Console'dan quota durumunuzu kontrol edin")
        print("   3. API planınızı yükseltmeyi düşünün")
        print("   4. Yeni bir API key oluşturmayı deneyin")
        print("\n💡 Script'i birkaç saat sonra tekrar çalıştırın, quota reset olmuş olabilir.")
        return []

    # Çeşitli promptları yükle
    prompts = load_diverse_prompts()
    
    # Eğer hedef sayıdan fazla prompt varsa, rastgele seç
    if len(prompts) > count:
        import random
        prompts = random.sample(prompts, count)
        print(f"✓ {count} adet prompt rastgele seçildi")
    
    # BASİT YAKLAŞIM: Thread pool yerine direkt döngü (daha stabil)
    # Thread pool bazen takılıyor, bu yüzden basit döngü kullanıyoruz
    
    # Checkpoint yükle
    ai_texts = load_checkpoint()
    existing_count = len(ai_texts)
    target_total = existing_count + count  # Toplam hedef
    
    # Duplicate kontrolü için mevcut metinleri set'e al (hızlı arama için)
    # Bu sayede yeni API key ile bile veri tekrarı olmaz
    existing_texts = set()
    for item in ai_texts:
        if 'text' in item:
            # Metni normalize et (başlangıç/son boşlukları temizle)
            normalized_text = item['text'].strip()
            if normalized_text:
                existing_texts.add(normalized_text)
    
    if existing_texts:
        print(f"✓ {len(existing_texts)} adet mevcut veri duplicate kontrolü için hazırlandı")
    
    print(f"\nMevcut AI verileri: {existing_count} adet")
    print(f"Yeni eklenecek: {count} adet")
    print(f"Toplam hedef: {target_total} adet")
    print(f"İstek Aralığı: {MIN_REQUEST_INTERVAL} saniye (Kotayı korumak için)")
    print(f"\n⚠ BASİT MOD: Thread pool yerine direkt döngü kullanılıyor (daha stabil)")
    
    # BASİT DÖNGÜ YAKLAŞIMI
    new_added_count = 0
    last_save_count = len(ai_texts)
    last_request_time = 0.0
    
    with tqdm(total=count, initial=0, desc="Yeni AI Üretimi") as pbar:
        prompt_idx = 0
        retry_count = 0
        max_retries_per_item = 3
        
        while new_added_count < count:
            # Prompt seç
            current_prompt = prompts[prompt_idx % len(prompts)]
            prompt_idx += 1
            
            # Rate limiting
            current_time = time.time()
            if last_request_time > 0:
                time_since_last = current_time - last_request_time
                if time_since_last < MIN_REQUEST_INTERVAL:
                    sleep_needed = MIN_REQUEST_INTERVAL - time_since_last
                    print(f"\n[DEBUG] Rate limiting: {sleep_needed:.1f} saniye bekleniyor...")
                    time.sleep(sleep_needed)
            else:
                # İlk istek için özel mesaj
                print(f"\n[DEBUG] İlk API isteği yapılıyor (bekleme yok)...")
            
            # API çağrısı - direkt yap
            print(f"\n[DEBUG] İstek {new_added_count + 1}/{count} gönderiliyor...", flush=True)
            print(f"[DEBUG] Prompt: {current_prompt[:50]}...", flush=True)
            print(f"[DEBUG] Model: {selected_model_name}", flush=True)
            
            try:
                request_start_time = time.time()
                last_request_time = time.time()
                
                # API çağrısı - direkt (timeout problemi nedeni ile basit çağrı)
                print(f"[DEBUG] API çağrısı başlatılıyor...", flush=True)
                sys.stdout.flush()
                sys.stderr.flush()
                
                try:
                    response = model.generate_content(current_prompt)
                except Exception as api_error:
                    print(f"[DEBUG] API HATASI: {api_error}", flush=True)
                    raise api_error
                
                request_duration = time.time() - request_start_time
                print(f"[DEBUG] API yanıtı alındı! Süre: {request_duration:.2f} saniye", flush=True)
                
                if response and hasattr(response, 'text'):
                    generated_text = response.text.strip()
                    
                    if len(generated_text) >= 50:
                        # Duplicate kontrolü
                        if generated_text not in existing_texts:
                            result = {
                                "text": generated_text,
                                "label": "AI",
                                "source": "gemini",
                                "prompt": current_prompt,
                                "generated_date": datetime.now().isoformat()
                            }
                            ai_texts.append(result)
                            existing_texts.add(generated_text)
                            new_added_count += 1
                            pbar.update(1)
                            retry_count = 0  # Başarılı, retry sayacını sıfırla
                            
                            print(f"[DEBUG] ✓ Başarılı! ({len(generated_text)} karakter)")
                            
                            # Düzenli kayıt
                            if len(ai_texts) - last_save_count >= CHECKPOINT_INTERVAL:
                                save_checkpoint(ai_texts)
                                last_save_count = len(ai_texts)
                                print(f"[DEBUG] Checkpoint kaydedildi: {len(ai_texts)} adet")
                        else:
                            print(f"[DEBUG] ⚠ Duplicate bulundu, bir sonraki prompt'a geçiliyor...")
                            retry_count = 0  # Duplicate için retry yok, direkt geç
                            continue  # Bir sonraki prompt'a geç
                    else:
                        print(f"[DEBUG] ⚠ Çok kısa metin ({len(generated_text)} karakter), bir sonraki prompt'a geçiliyor...")
                        retry_count = 0
                        continue  # Bir sonraki prompt'a geç
                else:
                    print(f"[DEBUG] ⚠ Boş yanıt, bir sonraki prompt'a geçiliyor...")
                    retry_count = 0
                    continue  # Bir sonraki prompt'a geç
                    
            except KeyboardInterrupt:
                print(f"\n⚠ Script kullanıcı tarafından durduruldu!")
                break
            except Exception as e:
                error_msg = str(e).lower()
                full_error = str(e)
                is_rate_limit = "429" in error_msg or "quota" in error_msg or "resource exhausted" in error_msg
                
                print(f"\n[DEBUG] Hata yakalandı: {full_error[:200]}")
                print(f"[DEBUG] Hata tipi: {type(e).__name__}")
                
                if is_rate_limit:
                    # Quota hatası - hata mesajından retry_delay'i çıkarmaya çalış
                    wait_time = 300  # Varsayılan 5 dakika
                    if "retry_delay" in full_error or "retry in" in full_error.lower():
                        # Hata mesajından saniye bilgisini çıkarmaya çalış
                        import re
                        retry_match = re.search(r'retry in ([\d.]+)s', full_error.lower())
                        if retry_match:
                            wait_time = max(int(float(retry_match.group(1))), 60)  # En az 60 saniye
                    
                    print(f"\n⚠ QUOTA HATASI TESPİT EDİLDİ!")
                    print(f"   Hata: {full_error[:150]}...")
                    print(f"   {int(wait_time/60)} dakika ({wait_time} saniye) bekleniyor...")
                    print(f"   💡 Quota genelde günlük reset olur (gece yarısı UTC)")
                    print(f"   💡 Alternatif: Yeni bir API key oluşturun")
                    time.sleep(wait_time)
                    retry_count = 0  # Quota hatası sonrası retry sayacını sıfırla, tekrar dene
                    continue  # Aynı prompt'u tekrar dene
                else:
                    retry_count += 1
                    if retry_count >= max_retries_per_item:
                        print(f"[DEBUG] ⚠ Bu prompt için {max_retries_per_item} deneme yapıldı, bir sonraki prompt'a geçiliyor...")
                        retry_count = 0
                        continue  # Bir sonraki prompt'a geç
                    wait_time = min(5 * (2 ** retry_count), 30)
                    print(f"⚠ Hata - {wait_time}sn bekleniyor (retry {retry_count}/{max_retries_per_item})...")
                    time.sleep(wait_time)
                    continue  # Aynı prompt'u tekrar dene
    
    # Final kayıt
    if len(ai_texts) > last_save_count:
        save_checkpoint(ai_texts)
    
    print(f"\n✓ Mevcut AI verileri: {existing_count} adet")
    print(f"✓ Yeni eklenen AI verileri: {new_added_count} adet")
    print(f"✓ Toplam AI verileri: {len(ai_texts)} adet")
    if new_added_count < count:
        print(f"⚠ Hedef: {count} yeni veri, Eklenen: {new_added_count} (Fark: {count - new_added_count})")
    
    return ai_texts

def save_data(data: List[Dict], filename: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # JSON
    json_path = os.path.join(OUTPUT_DIR, f"{filename}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # CSV (Opsiyonel, hata verirse program durmasın)
    try:
        df = pd.DataFrame(data)
        csv_path = os.path.join(OUTPUT_DIR, f"{filename}.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8')
    except Exception as e:
        print(f"CSV kaydı yapılamadı: {e}")
        
    print(f"✓ {filename} başarıyla kaydedildi.")

def load_checkpoint() -> List[Dict]:
    """
    Mevcut AI verilerini yükler. Öncelik sırası:
    1. Checkpoint dosyası
    2. ai_abstracts.json
    3. combined_dataset.csv'den AI verileri (eğer varsa)
    """
    # 1. Önce checkpoint dosyasını kontrol et
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data:
                    print(f"✓ Checkpoint yüklendi: {len(data)} adet mevcut veri bulundu")
                return data
        except Exception as e:
            print(f"⚠ Checkpoint yüklenirken hata: {e}")
    
    # 2. Checkpoint yoksa, mevcut ai_abstracts.json'dan yükle (eğer varsa)
    ai_abstracts_file = os.path.join(OUTPUT_DIR, "ai_abstracts.json")
    if os.path.exists(ai_abstracts_file):
        try:
            with open(ai_abstracts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data:
                    print(f"✓ Mevcut AI verileri yüklendi: {len(data)} adet (ai_abstracts.json'dan)")
                    # Checkpoint dosyasını geri oluştur
                    save_checkpoint(data)
                    print(f"✓ Checkpoint dosyası geri oluşturuldu")
                return data
        except Exception as e:
            print(f"⚠ AI verileri yüklenirken hata: {e}")
    
    # 3. JSON yoksa, combined_dataset.csv'den AI verilerini yükle
    combined_csv = os.path.join(OUTPUT_DIR, "combined_dataset.csv")
    if os.path.exists(combined_csv):
        try:
            import pandas as pd
            df = pd.read_csv(combined_csv)
            ai_data = df[df['label'] == 'AI'].to_dict(orient='records')
            if ai_data:
                # CSV'den gelen verileri JSON formatına çevir
                formatted_data = []
                for row in ai_data:
                    formatted_data.append({
                        "text": row.get('text', ''),
                        "label": "AI",
                        "source": row.get('source', 'gemini'),
                        "prompt": row.get('prompt', ''),
                        "generated_date": row.get('generated_date', '')
                    })
                print(f"✓ Mevcut AI verileri yüklendi: {len(formatted_data)} adet (combined_dataset.csv'den)")
                # Checkpoint dosyasını oluştur
                save_checkpoint(formatted_data)
                print(f"✓ Checkpoint dosyası oluşturuldu")
                return formatted_data
        except Exception as e:
            print(f"⚠ CSV'den veri yüklenirken hata: {e}")
    
    return []

def save_checkpoint(data: List[Dict]):
    try:
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

def main():
    # 1. Human verilerini kontrol et
    human_abstracts = load_human_abstracts()
    if not human_abstracts:
        print("⚠ Human verileri bulunamadı, sadece AI verileri üretilecek.")
    
    # 2. Mevcut AI verilerini yükle (checkpoint'ten)
    existing_ai_texts = load_checkpoint()
    existing_count = len(existing_ai_texts)
    
    # 3. Günlük batch boyutunu hesapla
    # Eğer günlük batch kullanılıyorsa, kalan veriye göre ayarla
    remaining_needed = AI_COUNT - (existing_count - 3000)  # 3000 = başlangıç sayısı
    if remaining_needed < 0:
        remaining_needed = 0
    
    # Günlük batch boyutunu kullan (eğer ayarlanmışsa)
    daily_batch = DAILY_BATCH_SIZE if DAILY_BATCH_SIZE < AI_COUNT else AI_COUNT
    target_count = min(daily_batch, remaining_needed) if remaining_needed > 0 else daily_batch
    
    if existing_count > 0:
        print(f"\n✓ Mevcut AI verileri: {existing_count} adet")
        if DAILY_BATCH_SIZE < AI_COUNT:
            print(f"  Günlük batch modu: {target_count} adet çekilecek")
            print(f"  Kalan: {remaining_needed} adet (birkaç güne yayılacak)")
        else:
            print(f"  Üzerine {AI_COUNT} adet yeni çeşitli AI verisi eklenecek")
        print(f"  Toplam hedef: {existing_count + AI_COUNT} AI verisi")
    else:
        print(f"\n✓ Yeni AI verileri üretilecek: {target_count} adet")

    # 4. Yeni AI Verisi Üret (mevcut verilerin üzerine ekle)
    # generate_ai_texts zaten load_checkpoint() ile mevcut verileri yükleyip üzerine ekliyor
    all_ai_texts = generate_ai_texts(target_count, GEMINI_API_KEY, MAX_WORKERS)
    
    # 4. AI verilerini kaydet
    if all_ai_texts:
        new_count = len(all_ai_texts) - existing_count
        
        print(f"\n{'='*60}")
        print("AI VERİLERİ KAYDEDİLİYOR")
        print(f"{'='*60}\n")
        print(f"Mevcut AI verileri: {existing_count} adet")
        print(f"Yeni eklenen AI verileri: {new_count} adet")
        print(f"Toplam AI verileri: {len(all_ai_texts)} adet")
        
        # AI verilerini kaydet
        save_data(all_ai_texts, "ai_abstracts")
        
        # 5. Birleştirilmiş veri seti oluştur ve kaydet
        if human_abstracts:
            print(f"\n{'='*60}")
            print("BİRLEŞTİRİLMİŞ VERİ SETİ OLUŞTURULUYOR")
            print(f"{'='*60}\n")
            all_data = human_abstracts + all_ai_texts
            save_data(all_data, "combined_dataset")
        
        # 6. Temizlik - Sadece tüm işlem tamamlandığında checkpoint'i sil
        total_new = len(all_ai_texts) - 3000  # 3000 = başlangıç sayısı
        if total_new >= AI_COUNT:
            if os.path.exists(CHECKPOINT_FILE):
                os.remove(CHECKPOINT_FILE)
                print(f"\n✓ Checkpoint dosyası temizlendi (tüm yeni veriler toplandı)")
        else:
            print(f"\n⚠ Checkpoint dosyası korunuyor (kaldığı yerden devam için)")
            print(f"   - Bugün eklenen: {new_count} AI verisi")
            print(f"   - Toplam yeni: {total_new}/{AI_COUNT} AI verisi")
            if DAILY_BATCH_SIZE < AI_COUNT:
                remaining = AI_COUNT - total_new
                days_needed = (remaining + DAILY_BATCH_SIZE - 1) // DAILY_BATCH_SIZE  # Yuvarlama
                print(f"   - Kalan: {remaining} veri (yaklaşık {days_needed} gün daha)")
            print(f"   - Checkpoint: {CHECKPOINT_FILE}")
            print(f"\n💡 İPUCU: Yarın script'i tekrar çalıştırın, kaldığı yerden devam edecek!")
        
        # İstatistikler
        print(f"\n{'='*60}")
        print("TOPLAMA İSTATİSTİKLERİ")
        print("=" * 60)
        if human_abstracts:
            print(f"İnsan yazımı örnekler: {len(human_abstracts)}")
        print(f"Mevcut AI örnekler: {existing_count}")
        print(f"Yeni eklenen AI örnekler: {new_count}")
        print(f"Toplam AI örnekler: {len(all_ai_texts)}")
        if human_abstracts:
            print(f"Toplam veri seti: {len(human_abstracts) + len(all_ai_texts)}")
            print(f"Oran (Human:AI): {len(human_abstracts)}:{len(all_ai_texts)}")
        print(f"Veri seti kaydedildi: {OUTPUT_DIR}")
        print("=" * 60)
    else:
        print("\n⚠ Yeni AI verisi üretilemedi!")

if __name__ == "__main__":
    main()