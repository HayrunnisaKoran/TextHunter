"""
Veri Seti Toplama Scripti
- ArXiv'den 3000 insan yazımı makale özeti toplar
- Gemini AI ile 3000 AI yazımı metin üretir
- Toplam 6000 örnek oluşturur
"""

import os
import json
import time
import arxiv
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import google.generativeai as genai
from typing import List, Dict

# Yapılandırma
ARXIV_COUNT = 3000  # İnsan yazımı makale sayısı
AI_COUNT = 3000     # AI yazımı makale sayısı
OUTPUT_DIR = "../Data/raw"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Ortam değişkeninden alınacak

# Lisans kontrolü için izin verilen lisanslar
ALLOWED_LICENSES = [
    "MIT License",
    "Apache 2.0",
    "BSD",
    "CC-BY",
    "CC0"
]

def collect_arxiv_abstracts(count: int = 3000) -> List[Dict]:
    """
    ArXiv'den makale özetleri toplar
    """
    print(f"ArXiv'den {count} makale özeti toplanıyor...")
    
    abstracts = []
    search = arxiv.Search(
        query="cat:cs.AI OR cat:cs.CL OR cat:cs.LG OR cat:stat.ML",
        max_results=count * 2,  # Daha fazla sonuç al, filtreleme için
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    collected = 0
    for result in tqdm(search.results(), total=count):
        if collected >= count:
            break
            
        try:
            # Özet uzunluğu kontrolü (çok kısa veya çok uzun olmasın)
            abstract_text = result.summary.strip()
            if len(abstract_text) < 100 or len(abstract_text) > 2000:
                continue
            
            abstract_data = {
                "text": abstract_text,
                "label": "Human",
                "source": "arxiv",
                "arxiv_id": result.entry_id,
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "published": result.published.isoformat(),
                "license": "CC-BY",  # ArXiv varsayılan olarak CC-BY
                "collected_date": datetime.now().isoformat()
            }
            
            abstracts.append(abstract_data)
            collected += 1
            
            # Rate limiting için kısa bekleme
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Hata: {e}")
            continue
    
    print(f"Toplam {len(abstracts)} makale özeti toplandı.")
    return abstracts

def generate_ai_texts(count: int = 3000, api_key: str = "") -> List[Dict]:
    """
    Gemini AI kullanarak akademik makale özetleri üretir
    """
    if not api_key:
        print("UYARI: GEMINI_API_KEY ortam değişkeni ayarlanmamış!")
        print("AI metinleri üretilemeyecek. Lütfen API anahtarınızı ayarlayın.")
        return []
    
    print(f"Gemini AI ile {count} metin üretiliyor...")
    
    genai.configure(api_key=api_key)
    
    # Güncel model isimlerini dene (sırayla)
    model_names = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
    model = None
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test isteği gönder
            test_response = model.generate_content("test")
            print(f"✓ Model '{model_name}' başarıyla yüklendi")
            break
        except Exception as e:
            print(f"⚠ Model '{model_name}' yüklenemedi: {e}")
            continue
    
    if model is None:
        print("❌ HATA: Hiçbir Gemini modeli yüklenemedi!")
        print("Lütfen API anahtarınızı ve internet bağlantınızı kontrol edin.")
        return []
    
    ai_texts = []
    
    # Farklı konular için prompt şablonları
    prompts = [
        "Write a detailed academic abstract about machine learning applications in natural language processing. The abstract should be between 150-500 words, include methodology, results, and conclusions.",
        "Write a comprehensive academic abstract about deep learning models for computer vision tasks. Include technical details, experimental setup, and key findings. Length: 150-500 words.",
        "Write an academic abstract about statistical methods in data science. Include research methodology, dataset description, and statistical analysis results. Length: 150-500 words.",
        "Write a detailed academic abstract about neural network architectures for time series prediction. Include model architecture, training procedure, and performance metrics. Length: 150-500 words.",
        "Write a comprehensive academic abstract about reinforcement learning algorithms. Include problem formulation, algorithm description, and experimental results. Length: 150-500 words.",
        "Write an academic abstract about transformer models and their applications. Include model architecture details, training methodology, and evaluation results. Length: 150-500 words.",
        "Write a detailed academic abstract about unsupervised learning techniques. Include methodology, experimental design, and comparative analysis. Length: 150-500 words.",
        "Write a comprehensive academic abstract about optimization algorithms in machine learning. Include algorithm description, convergence analysis, and experimental validation. Length: 150-500 words."
    ]
    
    consecutive_errors = 0
    max_consecutive_errors = 10
    
    for i in tqdm(range(count)):
        try:
            # Prompt'ları döngüsel olarak kullan
            prompt = prompts[i % len(prompts)]
            
            response = model.generate_content(prompt)
            
            # Response kontrolü
            if not response or not hasattr(response, 'text'):
                print(f"⚠ Uyarı: Boş yanıt alındı (iterasyon {i+1})")
                time.sleep(2)
                continue
            
            generated_text = response.text.strip()
            
            # Metin uzunluğu kontrolü
            if len(generated_text) < 100 or len(generated_text) > 2000:
                continue
            
            ai_data = {
                "text": generated_text,
                "label": "AI",
                "source": "gemini",
                "prompt": prompt,
                "generated_date": datetime.now().isoformat()
            }
            
            ai_texts.append(ai_data)
            consecutive_errors = 0  # Başarılı istek, hata sayacını sıfırla
            
            # Rate limiting
            time.sleep(1)  # Gemini API rate limit için
            
        except Exception as e:
            consecutive_errors += 1
            error_msg = str(e)
            
            # 404 hatası (model bulunamadı) durumunda scripti durdur
            if "404" in error_msg and "not found" in error_msg.lower():
                print(f"\n❌ KRİTİK HATA: Model bulunamadı!")
                print(f"Hata: {error_msg}")
                print("Lütfen scripti durdurun ve model adını kontrol edin.")
                break
            
            # Rate limit hatası
            if "rate limit" in error_msg.lower() or "429" in error_msg:
                print(f"\n⚠ Rate limit hatası - 5 saniye bekleniyor...")
                time.sleep(5)
                continue
            
            # Diğer hatalar
            if consecutive_errors <= 3:  # İlk 3 hatada detaylı mesaj
                print(f"\n⚠ Hata (AI üretimi, iterasyon {i+1}): {error_msg}")
            
            # Çok fazla ardışık hata varsa durdur
            if consecutive_errors >= max_consecutive_errors:
                print(f"\n❌ {max_consecutive_errors} ardışık hata alındı. İşlem durduruluyor.")
                print(f"Toplanan AI metin sayısı: {len(ai_texts)}")
                break
            
            time.sleep(2)  # Hata durumunda daha uzun bekleme
            continue
    
    print(f"Toplam {len(ai_texts)} AI metni üretildi.")
    return ai_texts

def save_data(data: List[Dict], filename: str):
    """
    Veriyi JSON ve CSV formatında kaydeder
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # JSON formatında kaydet
    json_path = os.path.join(OUTPUT_DIR, f"{filename}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # CSV formatında kaydet
    df = pd.DataFrame(data)
    csv_path = os.path.join(OUTPUT_DIR, f"{filename}.csv")
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"Veri kaydedildi: {json_path}")
    print(f"Veri kaydedildi: {csv_path}")

def main():
    """
    Ana fonksiyon - veri toplama işlemini yönetir
    """
    print("=" * 60)
    print("VERİ SETİ TOPLAMA BAŞLATILIYOR")
    print("=" * 60)
    
    # 1. ArXiv'den insan yazımı özetler
    human_abstracts = collect_arxiv_abstracts(ARXIV_COUNT)
    save_data(human_abstracts, "human_abstracts")
    
    # 2. AI ile metin üretimi
    ai_texts = generate_ai_texts(AI_COUNT, GEMINI_API_KEY)
    if ai_texts:
        save_data(ai_texts, "ai_abstracts")
    
    # 3. Birleştirilmiş veri seti
    all_data = human_abstracts + ai_texts
    save_data(all_data, "combined_dataset")
    
    # İstatistikler
    print("\n" + "=" * 60)
    print("TOPLAMA İSTATİSTİKLERİ")
    print("=" * 60)
    print(f"İnsan yazımı örnekler: {len(human_abstracts)}")
    print(f"AI yazımı örnekler: {len(ai_texts)}")
    print(f"Toplam örnek: {len(all_data)}")
    print(f"Veri seti kaydedildi: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

