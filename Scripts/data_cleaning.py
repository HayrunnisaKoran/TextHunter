"""
Veri Temizleme Scripti
- Ham veriyi temizler ve normalize eder
- Tokenizasyon ve ön işleme yapar
- Temizlenmiş veriyi kaydeder
"""

import os
import json
import pandas as pd
import re
import string
from typing import List, Dict
from tqdm import tqdm

INPUT_DIR = "../Data/raw"
OUTPUT_DIR = "../Data/cleaned"

def clean_text(text: str) -> str:
    """
    Metni temizler ve normalize eder
    """
    if not isinstance(text, str):
        return ""
    
    # Küçük harfe çevir
    text = text.lower()
    
    # URL'leri kaldır
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Email adreslerini kaldır
    text = re.sub(r'\S+@\S+', '', text)
    
    # Özel karakterleri ve sayıları koru ama fazla boşlukları temizle
    # Akademik metinlerde sayılar ve özel karakterler önemli olabilir
    
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text)
    
    # Başta ve sonda boşlukları kaldır
    text = text.strip()
    
    # Çok kısa metinleri filtrele
    if len(text) < 50:
        return ""
    
    return text

def remove_duplicates(data: List[Dict]) -> List[Dict]:
    """
    Tekrarlanan metinleri kaldırır
    """
    seen_texts = set()
    unique_data = []
    
    for item in data:
        text = item.get('text', '').strip()
        if text and text not in seen_texts:
            seen_texts.add(text)
            unique_data.append(item)
    
    return unique_data

def balance_dataset(data: List[Dict]) -> List[Dict]:
    """
    Veri setini dengeler (Human ve AI sayılarını eşitler)
    """
    human_data = [item for item in data if item.get('label') == 'Human']
    ai_data = [item for item in data if item.get('label') == 'AI']
    
    print(f"Temizleme öncesi - Human: {len(human_data)}, AI: {len(ai_data)}")
    
    # Daha az olan sınıfın sayısına göre dengele
    min_count = min(len(human_data), len(ai_data))
    
    balanced_data = human_data[:min_count] + ai_data[:min_count]
    
    print(f"Temizleme sonrası - Human: {min_count}, AI: {min_count}, Toplam: {len(balanced_data)}")
    
    return balanced_data

def validate_data(data: List[Dict]) -> List[Dict]:
    """
    Veriyi doğrular ve geçersiz örnekleri kaldırır
    """
    valid_data = []
    
    for item in tqdm(data, desc="Veri doğrulama"):
        text = item.get('text', '')
        label = item.get('label', '')
        
        # Gerekli alanlar kontrolü
        if not text or not label:
            continue
        
        # Metin uzunluğu kontrolü
        if len(text) < 50 or len(text) > 5000:
            continue
        
        # Label kontrolü
        if label not in ['Human', 'AI']:
            continue
        
        valid_data.append(item)
    
    return valid_data

def process_dataset(input_file: str, output_file: str):
    """
    Veri setini işler ve temizler
    """
    print(f"Veri yükleniyor: {input_file}")
    
    # JSON veya CSV dosyasını yükle
    if input_file.endswith('.json'):
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif input_file.endswith('.csv'):
        df = pd.read_csv(input_file, encoding='utf-8')
        data = df.to_dict('records')
    else:
        raise ValueError("Desteklenmeyen dosya formatı. JSON veya CSV olmalı.")
    
    print(f"Yüklenen örnek sayısı: {len(data)}")
    
    # 1. Metinleri temizle
    print("\nMetinler temizleniyor...")
    for item in tqdm(data, desc="Temizleme"):
        if 'text' in item:
            item['text'] = clean_text(item['text'])
    
    # 2. Boş metinleri kaldır
    data = [item for item in data if item.get('text', '').strip()]
    print(f"Temizleme sonrası örnek sayısı: {len(data)}")
    
    # 3. Tekrarları kaldır
    print("\nTekrarlar kaldırılıyor...")
    data = remove_duplicates(data)
    print(f"Tekrar kaldırma sonrası örnek sayısı: {len(data)}")
    
    # 4. Veri doğrulama
    print("\nVeri doğrulanıyor...")
    data = validate_data(data)
    print(f"Doğrulama sonrası örnek sayısı: {len(data)}")
    
    # 5. Veri setini dengele
    print("\nVeri seti dengeleniyor...")
    data = balance_dataset(data)
    
    # 6. İstatistikler
    human_count = sum(1 for item in data if item.get('label') == 'Human')
    ai_count = sum(1 for item in data if item.get('label') == 'AI')
    
    print("\n" + "=" * 60)
    print("TEMİZLEME İSTATİSTİKLERİ")
    print("=" * 60)
    print(f"Toplam örnek: {len(data)}")
    print(f"Human: {human_count}")
    print(f"AI: {ai_count}")
    print(f"Ortalama metin uzunluğu: {sum(len(item.get('text', '')) for item in data) / len(data):.1f}")
    
    # 7. Kaydet
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # JSON formatında kaydet
    json_path = os.path.join(OUTPUT_DIR, f"{output_file}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # CSV formatında kaydet
    df = pd.DataFrame(data)
    csv_path = os.path.join(OUTPUT_DIR, f"{output_file}.csv")
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"\nTemizlenmiş veri kaydedildi:")
    print(f"  - {json_path}")
    print(f"  - {csv_path}")

def main():
    """
    Ana fonksiyon
    """
    print("=" * 60)
    print("VERİ TEMİZLEME BAŞLATILIYOR")
    print("=" * 60)
    
    input_file = os.path.join(INPUT_DIR, "combined_dataset.json")
    
    if not os.path.exists(input_file):
        # CSV dosyasını dene
        input_file = os.path.join(INPUT_DIR, "combined_dataset.csv")
        if not os.path.exists(input_file):
            print(f"HATA: Veri dosyası bulunamadı: {input_file}")
            print("Lütfen önce veri toplama scriptini çalıştırın.")
            return
    
    process_dataset(input_file, "cleaned_dataset")

if __name__ == "__main__":
    main()

