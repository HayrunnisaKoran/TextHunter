import os
import json
import random
import time
from datetime import datetime
from tqdm import tqdm
import requests
import concurrent.futures  # Hızın sırrı bu kütüphane

# --- AYARLAR ---
OUTPUT_DIR = "../Data/raw"
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "ai_abstracts_checkpoint.json")
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"  # Hızlı model
TARGET_DATA_COUNT = 3620
BATCH_SAVE_INTERVAL = 10
MAX_WORKERS = 4  # <-- BURASI ÖNEMLİ: Aynı anda 4 üretim yapacak

# Konular (Senin listenin aynısı)
TOPICS = {
    "History": [
        "Write a detailed academic abstract about the Roman Empire's political structure. 150-300 words.",
        "Write a comprehensive academic abstract about the Industrial Revolution. 150-300 words.",
        "Write an academic abstract analyzing the Cold War. 150-300 words.",
        "Write a detailed academic abstract about Ottoman Architecture. 150-300 words.",
        "Write a comprehensive academic abstract about Mayan Civilization. 150-300 words.",
        "Write an academic abstract about Medieval European feudal systems. 150-300 words.",
    ],
    "Biology": [
        "Write a detailed academic abstract about photosynthesis. 150-300 words.",
        "Write a comprehensive academic abstract about CRISPR gene editing. 150-300 words.",
        "Write an academic abstract analyzing marine ecosystems. 150-300 words.",
        "Write a detailed academic abstract about viral transmission. 150-300 words.",
        "Write a comprehensive academic abstract about cellular respiration. 150-300 words.",
        "Write an academic abstract about DNA structure. 150-300 words.",
    ],
    "Economics": [
        "Write a detailed academic abstract about inflation dynamics. 150-300 words.",
        "Write a comprehensive academic abstract about cryptocurrency markets. 150-300 words.",
        "Write an academic abstract analyzing supply chain management. 150-300 words.",
        "Write a detailed academic abstract about microfinance. 150-300 words.",
        "Write a comprehensive academic abstract about game theory. 150-300 words.",
        "Write an academic abstract about international trade. 150-300 words.",
    ],
     "Psychology": [
        "Write a detailed academic abstract about cognitive dissonance. 150-300 words.",
        "Write a comprehensive academic abstract about child development. 150-300 words.",
        "Write an academic abstract analyzing behavioral therapy. 150-300 words.",
        "Write a detailed academic abstract about sleep disorders. 150-300 words.",
        "Write a comprehensive academic abstract about social influence. 150-300 words.",
        "Write an academic abstract about depression and anxiety. 150-300 words.",
    ],
    "Physics": [
        "Write a detailed academic abstract about quantum mechanics. 150-300 words.",
        "Write a comprehensive academic abstract about thermodynamics. 150-300 words.",
        "Write an academic abstract analyzing dark matter. 150-300 words.",
        "Write a detailed academic abstract about renewable energy. 150-300 words.",
        "Write a comprehensive academic abstract about fluid dynamics. 150-300 words.",
        "Write an academic abstract about relativity theory. 150-300 words.",
    ],
    "Literature": [
        "Write a detailed academic abstract about Shakespearean tragedy. 150-300 words.",
        "Write a comprehensive academic abstract about post-modernism. 150-300 words.",
        "Write an academic abstract analyzing haiku poetry. 150-300 words.",
        "Write a detailed academic abstract about dystopian novels. 150-300 words.",
        "Write a comprehensive academic abstract about Greek mythology. 150-300 words.",
        "Write an academic abstract about narrative structure. 150-300 words.",
    ],
    "Medicine": [
        "Write a detailed academic abstract about cardiovascular health. 150-300 words.",
        "Write a comprehensive academic abstract about vaccine efficacy. 150-300 words.",
        "Write an academic abstract analyzing neurological disorders. 150-300 words.",
        "Write a detailed academic abstract about robotic surgery. 150-300 words.",
        "Write a comprehensive academic abstract about public health policies. 150-300 words.",
        "Write an academic abstract about cancer biology. 150-300 words.",
    ],
    "Geology": [
        "Write a detailed academic abstract about plate tectonics. 150-300 words.",
        "Write a comprehensive academic abstract about volcanic eruptions. 150-300 words.",
        "Write an academic abstract analyzing climate change impact. 150-300 words.",
        "Write a detailed academic abstract about soil erosion. 150-300 words.",
        "Write a comprehensive academic abstract about mineral formation. 150-300 words.",
        "Write an academic abstract about earthquakes. 150-300 words.",
    ],
    "Art": [
        "Write a detailed academic abstract about Renaissance painting. 150-300 words.",
        "Write a comprehensive academic abstract about digital art trends. 150-300 words.",
        "Write an academic abstract analyzing Impressionism. 150-300 words.",
        "Write a detailed academic abstract about sculpture techniques. 150-300 words.",
        "Write a comprehensive academic abstract about color theory. 150-300 words.",
        "Write an academic abstract about contemporary art. 150-300 words.",
    ],
    "Computer Science": [
        "Write a detailed academic abstract about cloud computing. 150-300 words.",
        "Write a comprehensive academic abstract about cybersecurity. 150-300 words.",
        "Write an academic abstract analyzing blockchain technology. 150-300 words.",
        "Write a detailed academic abstract about IoT devices. 150-300 words.",
        "Write a comprehensive academic abstract about big data analytics. 150-300 words.",
        "Write an academic abstract about artificial intelligence. 150-300 words.",
    ],
}

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_checkpoint(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_single_item(item_data):
    """Tek bir veriyi üretir (Paralel çalışacak fonksiyon)"""
    prompt = item_data["prompt"]
    topic = item_data["topic"]
    
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": 2048, "temperature": 0.8}
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            text = result.get('response', '').strip()
            if len(text) > 50:
                return {
                    "text": text,
                    "label": "AI",
                    "source": "ollama",
                    "model": OLLAMA_MODEL,
                    "topic": topic,
                    "prompt": prompt,
                    "generated_date": datetime.now().isoformat()
                }
    except:
        pass
    return None

def main():
    print(f"=== {OLLAMA_MODEL} ile HIZLI Üretim Başlıyor ===")
    
    ai_texts = load_checkpoint()
    existing_texts = {item['text'].strip() for item in ai_texts if 'text' in item}
    
    total_needed = TARGET_DATA_COUNT - len(ai_texts)
    print(f"Hedef: {TARGET_DATA_COUNT}, Kalan: {total_needed}")
    
    if total_needed <= 0:
        return

    # İş kuyruğu oluştur
    queue = []
    topics_list = list(TOPICS.items())
    while len(queue) < total_needed + 100:
        topic, prompts = random.choice(topics_list)
        queue.append({"topic": topic, "prompt": random.choice(prompts)})

    new_count = 0
    # BURASI SİHİRLİ KISIM: 4 işçi aynı anda çalışacak
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(generate_single_item, item) for item in queue]
        
        with tqdm(total=total_needed) as pbar:
            for future in concurrent.futures.as_completed(futures):
                if new_count >= total_needed:
                    break
                
                result = future.result()
                if result and result['text'] not in existing_texts:
                    ai_texts.append(result)
                    existing_texts.add(result['text'])
                    new_count += 1
                    pbar.update(1)
                    
                    if len(ai_texts) % BATCH_SAVE_INTERVAL == 0:
                        save_checkpoint(ai_texts)

    save_checkpoint(ai_texts)
    print("Bitti!")

if __name__ == "__main__":
    main()