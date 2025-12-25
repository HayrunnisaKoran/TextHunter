import pandas as pd
import os

ai_file = '../Data/raw/ai_abstracts.csv'
exists = os.path.exists(ai_file)
print('Dosya var mı?', exists)
print()

if exists:
    df = pd.read_csv(ai_file)
    print(f'Mevcut AI verisi sayısı: {len(df)}')
    print(f'Kolonlar: {list(df.columns)}')
    if 'prompt' in df.columns:
        print('\nİlk 3 prompt örneği:')
        for i, p in enumerate(df['prompt'].head(3), 1):
            print(f'{i}. {p[:100]}...')
else:
    print('AI verisi dosyası bulunamadı.')

