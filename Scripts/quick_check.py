import pandas as pd
import sys

try:
    h = pd.read_csv('../Data/raw/human_abstracts.csv')
    a = pd.read_csv('../Data/raw/ai_abstracts.csv')
    
    print('=== KESIN VERI SAYILARI ===')
    print(f'Human abstracts: {len(h)} adet')
    print(f'AI abstracts: {len(a)} adet')
    print(f'Toplam: {len(h) + len(a)} adet')
    print()
    print('=== GEREKSINIM KONTROLU ===')
    print(f'Gereksinim: 6000 (3000 Human + 3000 AI)')
    print()
    print(f'Human durumu: {"✅ TAMAM" if len(h) >= 3000 else "❌ EKSIK"} ({len(h)}/3000)')
    print(f'AI durumu: {"✅ TAMAM" if len(a) >= 3000 else "❌ EKSIK"} ({len(a)}/3000)')
    print(f'Toplam durumu: {"✅ TAMAM" if (len(h) + len(a)) >= 6000 else "❌ EKSIK"} ({(len(h) + len(a))}/6000)')
    print()
    print('=== LABEL KONTROLU ===')
    if 'label' in h.columns:
        print('Human labels:')
        print(h['label'].value_counts())
    if 'label' in a.columns:
        print('AI labels:')
        print(a['label'].value_counts())
except Exception as e:
    print(f'Hata: {e}')
    sys.exit(1)
