"""
Veri tekrarı kontrolü ve temizleme scripti
"""

import pandas as pd
import json
import os
from pathlib import Path

DATA_DIR = Path("../Data/raw")

def check_duplicates_csv(file_path, name):
    """CSV dosyasında duplicate kontrolü yapar"""
    print(f"\n{'='*60}")
    print(f"{name} - CSV Kontrolü")
    print(f"{'='*60}")
    
    if not file_path.exists():
        print(f"⚠ Dosya bulunamadı: {file_path}")
        return None
    
    try:
        df = pd.read_csv(file_path)
        total_rows = len(df)
        
        # Text kolonunda duplicate kontrolü
        if 'text' in df.columns:
            unique_texts = df['text'].nunique()
            duplicates = df[df.duplicated(subset=['text'], keep=False)]
            duplicate_count = len(duplicates)
            
            print(f"Toplam satır sayısı (pandas): {total_rows}")
            print(f"Unique text sayısı: {unique_texts}")
            print(f"Duplicate veri sayısı: {duplicate_count}")
            
            if duplicate_count > 0:
                print(f"\n⚠ DUPLICATE BULUNDU!")
                print(f"Duplicate örnekleri:")
                print(duplicates[['text', 'label']].head(5).to_string())
                return df, duplicates
            else:
                print(f"✓ Duplicate YOK - Tüm veriler unique")
                return df, None
        else:
            print(f"⚠ 'text' kolonu bulunamadı")
            print(f"Kolonlar: {list(df.columns)}")
            return df, None
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None, None

def check_duplicates_json(file_path, name):
    """JSON dosyasında duplicate kontrolü yapar"""
    print(f"\n{'='*60}")
    print(f"{name} - JSON Kontrolü")
    print(f"{'='*60}")
    
    if not file_path.exists():
        print(f"⚠ Dosya bulunamadı: {file_path}")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_count = len(data)
        texts = [item.get('text', '').strip() for item in data if 'text' in item]
        unique_texts = len(set(texts))
        duplicate_count = total_count - unique_texts
        
        print(f"Toplam veri sayısı: {total_count}")
        print(f"Unique text sayısı: {unique_texts}")
        print(f"Duplicate veri sayısı: {duplicate_count}")
        
        if duplicate_count > 0:
            print(f"\n⚠ DUPLICATE BULUNDU!")
            # Duplicate'leri bul
            seen = set()
            duplicates = []
            for item in data:
                text = item.get('text', '').strip()
                if text in seen:
                    duplicates.append(item)
                else:
                    seen.add(text)
            
            print(f"Duplicate örnekleri (ilk 3):")
            for i, dup in enumerate(duplicates[:3], 1):
                print(f"\n{i}. Text: {dup.get('text', '')[:100]}...")
                print(f"   Label: {dup.get('label', '')}")
                print(f"   Date: {dup.get('generated_date', '')}")
            
            return data, duplicates
        else:
            print(f"✓ Duplicate YOK - Tüm veriler unique")
            return data, None
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None, None

def main():
    print("\n" + "="*60)
    print("VERİ TEKRARI (DUPLICATE) KONTROLÜ")
    print("="*60)
    
    # 1. Human Abstracts CSV
    human_csv = DATA_DIR / "human_abstracts.csv"
    df_human, dup_human = check_duplicates_csv(human_csv, "Human Abstracts")
    
    # 2. AI Abstracts CSV
    ai_csv = DATA_DIR / "ai_abstracts.csv"
    df_ai, dup_ai = check_duplicates_csv(ai_csv, "AI Abstracts")
    
    # 3. Combined Dataset CSV
    combined_csv = DATA_DIR / "combined_dataset.csv"
    df_combined, dup_combined = check_duplicates_csv(combined_csv, "Combined Dataset")
    
    # 4. JSON dosyaları
    human_json = DATA_DIR / "human_abstracts.json"
    data_human_json, dup_human_json = check_duplicates_json(human_json, "Human Abstracts")
    
    ai_json = DATA_DIR / "ai_abstracts.json"
    data_ai_json, dup_ai_json = check_duplicates_json(ai_json, "AI Abstracts")
    
    # Özet
    print(f"\n{'='*60}")
    print("ÖZET")
    print(f"{'='*60}")
    
    has_duplicates = False
    if dup_human is not None and len(dup_human) > 0:
        print(f"⚠ Human CSV: {len(dup_human)} duplicate")
        has_duplicates = True
    if dup_ai is not None and len(dup_ai) > 0:
        print(f"⚠ AI CSV: {len(dup_ai)} duplicate")
        has_duplicates = True
    if dup_combined is not None and len(dup_combined) > 0:
        print(f"⚠ Combined CSV: {len(dup_combined)} duplicate")
        has_duplicates = True
    if dup_human_json is not None and len(dup_human_json) > 0:
        print(f"⚠ Human JSON: {len(dup_human_json)} duplicate")
        has_duplicates = True
    if dup_ai_json is not None and len(dup_ai_json) > 0:
        print(f"⚠ AI JSON: {len(dup_ai_json)} duplicate")
        has_duplicates = True
    
    if not has_duplicates:
        print("✓ Tüm dosyalarda duplicate YOK!")
    else:
        print("\n💡 Duplicate temizlemek için:")
        print("   python remove_duplicates.py")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

