"""
Veri seti istatistiklerini kontrol eden script
User Story-1 gereksinimlerini kontrol eder
"""

import json
import os

def check_dataset():
    """Veri seti istatistiklerini kontrol eder"""
    
    data_dir = "../Data/raw"
    combined_file = os.path.join(data_dir, "combined_dataset.json")
    human_file = os.path.join(data_dir, "human_abstracts.json")
    ai_file = os.path.join(data_dir, "ai_abstracts.json")
    
    print("=" * 70)
    print("USER STORY-1: VERİ SETİ TOPLAMA KONTROLÜ")
    print("=" * 70)
    print()
    
    # Combined dataset kontrolü
    if os.path.exists(combined_file):
        with open(combined_file, 'r', encoding='utf-8') as f:
            combined_data = json.load(f)
        
        human_count = len([x for x in combined_data if x.get('label') == 'Human'])
        ai_count = len([x for x in combined_data if x.get('label') == 'AI'])
        total = len(combined_data)
        
        print(f"📊 COMBINED DATASET İSTATİSTİKLERİ:")
        print(f"   Toplam örnek: {total}")
        print(f"   Human yazımı: {human_count}")
        print(f"   AI yazımı: {ai_count}")
        print()
        
        # Kaynak kontrolü
        human_sources = set([x.get('source', 'unknown') for x in combined_data if x.get('label') == 'Human'])
        ai_sources = set([x.get('source', 'unknown') for x in combined_data if x.get('label') == 'AI'])
        
        print(f"📁 KAYNAK BİLGİLERİ:")
        print(f"   Human kaynakları: {human_sources}")
        print(f"   AI kaynakları: {ai_sources}")
        print()
        
        # Lisans kontrolü
        human_with_license = [x for x in combined_data if x.get('label') == 'Human' and 'license' in x]
        print(f"📜 LİSANS BİLGİLERİ:")
        print(f"   Lisans bilgisi olan Human örnekler: {len(human_with_license)}/{human_count}")
        if human_with_license:
            licenses = set([x.get('license', 'unknown') for x in human_with_license])
            print(f"   Lisans türleri: {licenses}")
        print()
        
        # Gereksinim kontrolü
        print("✅ GEREKSİNİM KONTROLÜ:")
        requirements_met = True
        
        # 1. Toplam 6000 örnek
        if total >= 6000:
            print(f"   ✓ Toplam örnek sayısı: {total} >= 6000 ✅")
        else:
            print(f"   ✗ Toplam örnek sayısı: {total} < 6000 ❌")
            requirements_met = False
        
        # 2. 3000 Human
        if human_count >= 3000:
            print(f"   ✓ Human yazımı örnek: {human_count} >= 3000 ✅")
        else:
            print(f"   ✗ Human yazımı örnek: {human_count} < 3000 ❌")
            requirements_met = False
        
        # 3. 3000 AI
        if ai_count >= 3000:
            print(f"   ✓ AI yazımı örnek: {ai_count} >= 3000 ✅")
        else:
            print(f"   ✗ AI yazımı örnek: {ai_count} < 3000 ❌")
            requirements_met = False
        
        # 4. ArXiv kullanımı
        if 'arxiv' in human_sources:
            print(f"   ✓ ArXiv kullanılıyor (Human verileri için) ✅")
        else:
            print(f"   ✗ ArXiv kullanılmıyor ❌")
            requirements_met = False
        
        # 5. Gemini/LLM kullanımı
        if 'gemini' in ai_sources or any('ai' in s.lower() or 'llm' in s.lower() for s in ai_sources):
            print(f"   ✓ LLM (Gemini) kullanılıyor (AI verileri için) ✅")
        else:
            print(f"   ✗ LLM kullanılmıyor ❌")
            requirements_met = False
        
        # 6. Lisans kontrolü
        if len(human_with_license) > 0:
            print(f"   ✓ Lisans bilgisi mevcut ✅")
        else:
            print(f"   ⚠ Lisans bilgisi eksik (ArXiv varsayılan CC-BY kabul edilebilir) ⚠")
        
        print()
        print("=" * 70)
        if requirements_met:
            print("✅ USER STORY-1 GEREKSİNİMLERİ KARŞILANIYOR!")
        else:
            print("❌ USER STORY-1 GEREKSİNİMLERİ TAM OLARAK KARŞILANMIYOR!")
        print("=" * 70)
        
    else:
        print(f"❌ Combined dataset dosyası bulunamadı: {combined_file}")
    
    # Ayrı dosyalar kontrolü
    print()
    print("📂 AYRI DOSYALAR:")
    if os.path.exists(human_file):
        with open(human_file, 'r', encoding='utf-8') as f:
            human_data = json.load(f)
        print(f"   ✓ human_abstracts.json: {len(human_data)} örnek")
    else:
        print(f"   ✗ human_abstracts.json bulunamadı")
    
    if os.path.exists(ai_file):
        with open(ai_file, 'r', encoding='utf-8') as f:
            ai_data = json.load(f)
        print(f"   ✓ ai_abstracts.json: {len(ai_data)} örnek")
    else:
        print(f"   ✗ ai_abstracts.json bulunamadı")

if __name__ == "__main__":
    check_dataset()
