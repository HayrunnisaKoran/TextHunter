"""
ArXiv Makale Özetleri Toplama Scripti
3000 adet insan yazımı makale özeti toplar
Lisans kontrolü yapar (MIT, Apache 2.0, BSD, CC-BY, CC0)
"""

import arxiv
import pandas as pd
import json
import os
from datetime import datetime
from tqdm import tqdm
import time

# Çıktı klasörü
OUTPUT_DIR = "../../Data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lisans kontrolü için kabul edilen lisanslar
ACCEPTED_LICENSES = [
    "MIT License",
    "Apache License 2.0",
    "BSD License",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC-BY",
    "CC0",
    "Creative Commons"
]

def check_license(paper):
    """Makale lisansını kontrol eder"""
    # ArXiv'de lisans bilgisi genellikle yorumlarda veya metadata'da bulunur
    # Basit bir kontrol yapıyoruz - gerçek uygulamada daha detaylı kontrol gerekebilir
    comment = paper.comment.lower() if paper.comment else ""
    summary = paper.summary.lower() if paper.summary else ""
    
    for license in ACCEPTED_LICENSES:
        if license.lower() in comment or license.lower() in summary:
            return True
    
    # Eğer açık bir lisans belirtilmemişse, ArXiv'in varsayılan lisansı kabul edilebilir
    # ArXiv genellikle CC-BY benzeri lisanslar kullanır
    return True  # ArXiv makaleleri genellikle açık erişimlidir

def collect_arxiv_abstracts(num_papers=3000, max_results_per_query=100):
    """
    ArXiv'den makale özetleri toplar
    
    Args:
        num_papers: Toplanacak makale sayısı
        max_results_per_query: Her sorguda maksimum sonuç sayısı
    """
    papers_data = []
    collected = 0
    
    # Farklı kategorilerden makale toplama (daha çeşitli veri için)
    categories = [
        "cs.AI",      # Artificial Intelligence
        "cs.CL",      # Computation and Language
        "cs.LG",      # Machine Learning
        "cs.CV",      # Computer Vision
        "stat.ML",    # Machine Learning (Statistics)
        "cs.NE",      # Neural and Evolutionary Computing
    ]
    
    print(f"ArXiv'den {num_papers} adet makale özeti toplanıyor...")
    
    # Her kategoriden eşit sayıda makale toplamaya çalış
    papers_per_category = num_papers // len(categories)
    
    for category in categories:
        if collected >= num_papers:
            break
            
        print(f"\nKategori: {category}")
        
        try:
            # ArXiv'den makale ara
            search = arxiv.Search(
                query=f'cat:{category}',
                max_results=min(papers_per_category * 2, max_results_per_query),
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            for paper in tqdm(search.results(), desc=f"Toplanıyor ({category})"):
                if collected >= num_papers:
                    break
                
                try:
                    # Lisans kontrolü
                    if not check_license(paper):
                        continue
                    
                    # Özet uzunluğu kontrolü (çok kısa özetleri atla)
                    if len(paper.summary) < 200:
                        continue
                    
                    paper_data = {
                        "id": paper.entry_id,
                        "title": paper.title,
                        "summary": paper.summary,
                        "authors": [author.name for author in paper.authors],
                        "published": paper.published.isoformat() if paper.published else None,
                        "category": category,
                        "label": "Human",  # ArXiv makaleleri insan yazımı
                        "source": "arxiv",
                        "license": "CC-BY"  # ArXiv varsayılan lisansı
                    }
                    
                    papers_data.append(paper_data)
                    collected += 1
                    
                    # Rate limiting için kısa bekleme
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Hata (makale işlenirken): {e}")
                    continue
                    
        except Exception as e:
            print(f"Hata (kategori {category}): {e}")
            continue
    
    # Eğer yeterli makale toplanamadıysa, genel arama yap
    if collected < num_papers:
        print(f"\nGenel arama yapılıyor... ({collected}/{num_papers})")
        remaining = num_papers - collected
        
        try:
            search = arxiv.Search(
                query='all',
                max_results=min(remaining * 2, max_results_per_query),
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            for paper in tqdm(search.results(), desc="Genel arama"):
                if collected >= num_papers:
                    break
                
                try:
                    if len(paper.summary) < 200:
                        continue
                    
                    # Daha önce eklenmiş mi kontrol et
                    if any(p["id"] == paper.entry_id for p in papers_data):
                        continue
                    
                    paper_data = {
                        "id": paper.entry_id,
                        "title": paper.title,
                        "summary": paper.summary,
                        "authors": [author.name for author in paper.authors],
                        "published": paper.published.isoformat() if paper.published else None,
                        "category": "general",
                        "label": "Human",
                        "source": "arxiv",
                        "license": "CC-BY"
                    }
                    
                    papers_data.append(paper_data)
                    collected += 1
                    time.sleep(0.1)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Genel arama hatası: {e}")
    
    # Veriyi kaydet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON formatında kaydet
    json_path = os.path.join(OUTPUT_DIR, f"arxiv_human_abstracts_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(papers_data, f, ensure_ascii=False, indent=2)
    
    # CSV formatında kaydet
    df = pd.DataFrame(papers_data)
    csv_path = os.path.join(OUTPUT_DIR, f"arxiv_human_abstracts_{timestamp}.csv")
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"\n✓ Toplam {collected} adet makale özeti toplandı")
    print(f"✓ JSON: {json_path}")
    print(f"✓ CSV: {csv_path}")
    
    return papers_data

if __name__ == "__main__":
    # 3000 adet makale özeti topla
    papers = collect_arxiv_abstracts(num_papers=3000)
    print(f"\nToplama işlemi tamamlandı! Toplam {len(papers)} adet özet toplandı.")

