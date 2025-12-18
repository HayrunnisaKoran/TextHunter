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
from concurrent.futures import ThreadPoolExecutor
import threading
import random

# Özel Exception sınıfı
class QuotaExceededException(Exception):
    """API quota limiti aşıldığında fırlatılır"""
    pass

# --- YAPILANDIRMA (KRİTİK AYARLAR) ---
AI_COUNT = 3000
OUTPUT_DIR = "../Data/raw"
INPUT_FILE = os.path.join(OUTPUT_DIR, "human_abstracts.json")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "ai_abstracts_checkpoint.json")

# OPTİMİZASYON AYARLARI
# Yeni API anahtarı kullanıyorsanız daha hızlı toplama yapabilirsiniz
MAX_WORKERS = 1  # 1 thread - kota limitlerini önlemek için (en güvenli)
CHECKPOINT_INTERVAL = 10 # Veri kaybını önlemek için daha sık kayıt

# HIZ AYARLARI (Yeni API anahtarı için optimize edildi)
# Gemini API limitleri: ~15 istek/dakika (ücretsiz), ~60 istek/dakika (ücretli)
# Güvenli değer: 10 saniye (6 istek/dakika) - quota limitinden uzak kalır
# Agresif değer: 5 saniye (12 istek/dakika) - daha hızlı ama riskli
MIN_REQUEST_INTERVAL = 10.0  # 10 saniye (yeni API için güvenli ve hızlı)
# Eğer hala quota hatası alırsanız: 15.0 veya 20.0 yapın
# Eğer hiç hata almıyorsanız: 5.0 veya 7.0'ye düşürebilirsiniz 

def load_human_abstracts() -> List[Dict]:
    if not os.path.exists(INPUT_FILE):
        print(f"⚠ UYARI: {INPUT_FILE} dosyası bulunamadı!")
        return []
    
    print(f"Mevcut human verileri yükleniyor: {INPUT_FILE}")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        human_data = json.load(f)
    print(f"✓ {len(human_data)} adet human verisi yüklendi")
    return human_data

def generate_single_ai_text(model, prompt: str, lock: threading.Lock, last_request_time: List[float], 
                            min_interval: float) -> Dict:
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
                
                # Eğer son istekten beri yeterince zaman geçmediyse bekle
                if time_since_last < min_interval:
                    sleep_needed = min_interval - time_since_last
                    time.sleep(sleep_needed)
                
                # İsteği yapmadan hemen önce zamanı güncelle
                last_request_time[0] = time.time()

            # API çağrısı
            response = model.generate_content(prompt)
            
            if not response or not hasattr(response, 'text'):
                raise ValueError("Boş yanıt")
            
            generated_text = response.text.strip()
            
            # Basit kalite kontrolü
            if len(generated_text) < 50:
                raise ValueError("Çok kısa metin")

            return {
                "text": generated_text,
                "label": "AI",
                "source": "gemini",
                "prompt": prompt,
                "generated_date": datetime.now().isoformat()
            }

        except Exception as e:
            error_msg = str(e).lower()
            
            # 429 veya Quota hatası tespiti
            is_rate_limit = "429" in error_msg or "quota" in error_msg or "resource exhausted" in error_msg
            
            if attempt < max_retries - 1:
                if is_rate_limit:
                    # Quota hatası alındı - özel exception fırlat
                    raise QuotaExceededException("API quota limiti aşıldı")
                else:
                    # Diğer hatalar için daha kısa bekleme
                    wait_time = (base_wait_time * (2 ** attempt)) + random.uniform(0, 2)
                    wait_time = min(wait_time, 30)  # Max 30 saniye
                    print(f"\n⚠ Hata: {str(e)[:50]}... - {int(wait_time)}sn bekleniyor.")
                
                time.sleep(wait_time)
                continue
            
            return None # Tüm denemeler başarısız
    return None

def generate_ai_texts(count: int = 3000, api_key: str = "", max_workers: int = 2) -> List[Dict]:
    if not api_key:
        print("❌ HATA: GEMINI_API_KEY eksik!")
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
    
    # Öncelik sıralaması - önce güncel modeller, sonra eski modeller
    priority_models = [
        'gemini-2.5-flash',      # En yeni ve hızlı
        'gemini-2.0-flash',       # 2.0 Flash
        'gemini-2.5-pro',         # En yeni Pro
        'gemini-2.0-pro',         # 2.0 Pro
        'gemini-1.5-flash',       # Eski ama stabil
        'gemini-1.5-pro',         # Eski Pro
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
    for m_name in model_to_try:
        try:
            temp_model = genai.GenerativeModel(m_name)
            # Test isteği
            test_response = temp_model.generate_content("Hi")
            if test_response and hasattr(test_response, 'text'):
                model = temp_model
                selected_model_name = m_name
                print(f"✓ Model seçildi: {selected_model_name}")
                break
        except Exception as e:
            print(f"  - {m_name} kullanılamadı ({str(e)[:50]}...)")
            continue
            
    if not model:
        print("❌ Hiçbir model çalıştırılamadı. API Key veya Kotanızı kontrol edin.")
        print("\nÇözüm önerileri:")
        print("1. API anahtarınızın geçerli olduğundan emin olun")
        print("2. Mevcut modelleri görmek için: python list_gemini_models.py")
        print("3. İnternet bağlantınızı kontrol edin")
        return []

    # Prompt şablonları
    prompts = [
        "Write a detailed academic abstract about machine learning applications in natural language processing. 150-300 words.",
        "Write a comprehensive academic abstract about deep learning models for computer vision. 150-300 words.",
        "Write an academic abstract about statistical methods in data science. 150-300 words.",
        "Write a detailed academic abstract about neural network architectures for time series. 150-300 words.",
        "Write a comprehensive academic abstract about reinforcement learning algorithms. 150-300 words.",
        "Write an academic abstract about transformer models and LLMs. 150-300 words.",
        "Write a detailed academic abstract about unsupervised learning clustering. 150-300 words."
    ]
    
    # Thread senkronizasyonu için
    lock = threading.Lock()
    last_request_time = [0.0] # List kullanarak referans ile geçiyoruz
    
    # Checkpoint yükle
    ai_texts = load_checkpoint()
    start_index = len(ai_texts)
    
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
    
    print(f"\nBaşlangıç: {start_index}/{count}")
    print(f"Worker Sayısı: {max_workers}")
    print(f"İstek Aralığı: {MIN_REQUEST_INTERVAL} saniye (Kotayı korumak için)")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        from concurrent.futures import as_completed
        
        future_to_idx = {}
        retry_queue = []  # Başarısız olanları tekrar denemek için
        completed_count = start_index
        last_save_count = len(ai_texts)
        
        # İlk batch'i gönder (sadece worker sayısı kadar)
        next_index = start_index
        batch_size = max_workers * 2  # Her seferinde 2x worker kadar görev gönder
        
        def submit_batch(start_idx, end_idx):
            """Bir batch görev gönder"""
            for i in range(start_idx, min(end_idx, count)):
                p_idx = i % len(prompts)
                future = executor.submit(
                    generate_single_ai_text, 
                    model, 
                    prompts[p_idx], 
                    lock, 
                    last_request_time, 
                    MIN_REQUEST_INTERVAL
                )
                future_to_idx[future] = i
        
        # İlk batch'i gönder
        submit_batch(next_index, next_index + batch_size)
        next_index += batch_size
        
        # Sonuçları topla
        quota_exceeded = False  # Quota hatası flag'i
        with tqdm(total=count, initial=start_index, desc="AI Üretimi") as pbar:
            while completed_count < count and not quota_exceeded:
                # Tamamlanan görevleri kontrol et
                for future in list(future_to_idx.keys()):
                    if future.done():
                        idx = future_to_idx.pop(future)
                        try:
                            result = future.result()
                            
                            if result:
                                # Duplicate kontrolü - aynı metin zaten varsa ekleme
                                # Bu sayede yeni API key ile bile veri tekrarı olmaz
                                result_text = result.get('text', '').strip()
                                if result_text and result_text not in existing_texts:
                                    ai_texts.append(result)
                                    existing_texts.add(result_text)  # Set'e ekle (gelecek kontroller için)
                                    completed_count += 1
                                    pbar.update(1)
                                    
                                    # Düzenli Kayıt
                                    if len(ai_texts) - last_save_count >= CHECKPOINT_INTERVAL:
                                        save_checkpoint(ai_texts)
                                        last_save_count = len(ai_texts)
                                        pbar.set_postfix({"Kaydedilen": len(ai_texts), "Başarısız": len(retry_queue)})
                                else:
                                    # Duplicate bulundu - retry queue'ya ekle (yeni veri üretmek için)
                                    if result_text in existing_texts:
                                        pbar.set_postfix({"Kaydedilen": len(ai_texts), "Duplicate": 1})
                                    retry_queue.append(idx)
                                    completed_count += 1
                                    pbar.update(1)
                            else:
                                # Başarısız - retry queue'ya ekle
                                retry_queue.append(idx)
                                completed_count += 1
                                pbar.update(1)
                        except QuotaExceededException:
                            # Quota hatası - tüm işlemi durdur
                            quota_exceeded = True
                            break
                        except Exception as e:
                            # Diğer hatalar - retry queue'ya ekle
                            retry_queue.append(idx)
                            completed_count += 1
                            pbar.update(1)
                
                if quota_exceeded:
                    break
                
                # Retry queue'dan tekrar dene (boş slot varsa) - quota kontrolü ile
                while retry_queue and len(future_to_idx) < batch_size and next_index < count and not quota_exceeded:
                    idx = retry_queue.pop(0)
                    p_idx = idx % len(prompts)
                    future = executor.submit(
                        generate_single_ai_text, 
                        model, 
                        prompts[p_idx], 
                        lock, 
                        last_request_time, 
                        MIN_REQUEST_INTERVAL * 1.5  # Retry'da biraz daha uzun bekle
                    )
                    future_to_idx[future] = idx
                
                if quota_exceeded:
                    break
                
                # Yeni batch gönder (boş slot varsa) - quota kontrolü ile
                while len(future_to_idx) < batch_size and next_index < count and not quota_exceeded:
                    p_idx = next_index % len(prompts)
                    future = executor.submit(
                        generate_single_ai_text, 
                        model, 
                        prompts[p_idx], 
                        lock, 
                        last_request_time, 
                        MIN_REQUEST_INTERVAL
                    )
                    future_to_idx[future] = next_index
                    next_index += 1
                
                # Kısa bekleme (CPU kullanımını azaltmak için)
                if not future_to_idx:
                    break
                time.sleep(0.1)

    # Quota hatası kontrolü
    if quota_exceeded:
        # Final kayıt (mevcut verileri kaydet)
        if len(ai_texts) > last_save_count:
            save_checkpoint(ai_texts)
        
        print(f"\n{'='*60}")
        print("❌ API QUOTA LİMİTİ AŞILMIŞ - İŞLEM DURDURULDU")
        print(f"{'='*60}")
        print("\n⚠ API quota limitiniz aşılmış görünüyor.")
        print("   Bu durumda script çalışmaya devam edemez.")
        print("\n📋 ÇÖZÜM ÖNERİLERİ:")
        print("   1. Birkaç saat bekleyin (quota genelde saatlik/günlük reset olur)")
        print("   2. Google Cloud Console'dan quota durumunuzu kontrol edin")
        print("   3. API planınızı yükseltmeyi düşünün")
        print(f"\n💾 MEVCUT DURUM:")
        print(f"   - Toplanan veri: {len(ai_texts)} adet")
        print(f"   - Checkpoint dosyası: {CHECKPOINT_FILE}")
        print(f"   - Veriler güvende, quota reset olduktan sonra kaldığı yerden devam edebilirsiniz")
        print(f"\n{'='*60}\n")
        return ai_texts  # Mevcut verileri döndür
    
    # Final kayıt
    if len(ai_texts) > last_save_count:
        save_checkpoint(ai_texts)
    
    print(f"\n✓ Toplam {len(ai_texts)} AI metni üretildi.")
    if len(ai_texts) < count:
        print(f"⚠ Hedef: {count}, Üretilen: {len(ai_texts)} (Fark: {count - len(ai_texts)})")
        if retry_queue:
            print(f"⚠ {len(retry_queue)} istek başarısız oldu ve retry edilemedi.")
    
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
            ai_data = df[df['label'] == 'AI'].to_dict('records')
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
        return

    # 2. AI Verisi Üret
    ai_texts = generate_ai_texts(AI_COUNT, GEMINI_API_KEY, MAX_WORKERS)
    
    # 3. AI verilerini ayrı dosyaya kaydet (her zaman)
    if ai_texts:
        print(f"\n{'='*60}")
        print("AI VERİLERİ KAYDEDİLİYOR")
        print(f"{'='*60}\n")
        save_data(ai_texts, "ai_abstracts")
        
        # 4. Birleştirilmiş veri seti oluştur ve kaydet
        print(f"\n{'='*60}")
        print("BİRLEŞTİRİLMİŞ VERİ SETİ OLUŞTURULUYOR")
        print(f"{'='*60}\n")
        all_data = human_abstracts + ai_texts
        save_data(all_data, "combined_dataset")
        
        # 5. Temizlik - Sadece tüm işlem tamamlandığında checkpoint'i sil
        if len(ai_texts) >= AI_COUNT:
            if os.path.exists(CHECKPOINT_FILE):
                os.remove(CHECKPOINT_FILE)
                print(f"\n✓ Checkpoint dosyası temizlendi (tüm veriler toplandı)")
        else:
            print(f"\n⚠ Checkpoint dosyası korunuyor (kaldığı yerden devam için)")
            print(f"   - Mevcut: {len(ai_texts)}/{AI_COUNT} AI verisi")
            print(f"   - Checkpoint: {CHECKPOINT_FILE}")
        
        # İstatistikler
        print(f"\n{'='*60}")
        print("TOPLAMA İSTATİSTİKLERİ")
        print("=" * 60)
        print(f"İnsan yazımı örnekler: {len(human_abstracts)}")
        print(f"AI yazımı örnekler: {len(ai_texts)}")
        print(f"Toplam örnek: {len(all_data)}")
        print(f"Veri seti kaydedildi: {OUTPUT_DIR}")
        print("=" * 60)

if __name__ == "__main__":
    main()