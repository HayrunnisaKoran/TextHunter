"""
Çeşitli Konulardan Prompt Oluşturma Scripti
Kullanıcının verdiği örneğe benzer şekilde, çeşitli akademik disiplinlerden promptlar oluşturur.
"""

import pandas as pd
import random

# 1. Konu Başlıklarını Çeşitlendir (Sadece AI değil!)
topics = {
    "History": ["Roman Empire", "Industrial Revolution", "Cold War", "Ottoman Architecture", "Mayan Civilization"],
    "Biology": ["Photosynthesis", "CRISPR gene editing", "Marine ecosystems", "Viral transmission", "Cellular respiration"],
    "Economics": ["Inflation dynamics", "Crypto markets", "Supply chain management", "Microfinance", "Game theory"],
    "Psychology": ["Cognitive dissonance", "Child development", "Behavioral therapy", "Sleep disorders", "Social influence"],
    "Physics": ["Quantum mechanics", "Thermodynamics", "Dark matter", "Renewable energy", "Fluid dynamics"],
    "Literature": ["Shakespearean tragedy", "Post-modernism", "Haiku poetry structure", "Dystopian novels", "Greek mythology"],
    "Medicine": ["Cardiovascular health", "Vaccine efficacy", "Neurological disorders", "Robotic surgery", "Public health policies"],
    "Geology": ["Plate tectonics", "Volcanic eruptions", "Climate change impact", "Soil erosion", "Mineral formation"],
    "Art": ["Renaissance painting", "Digital art trends", "Impressionism", "Sculpture techniques", "Color theory"],
    "Computer Science": ["Cloud computing", "Cybersecurity", "Blockchain", "IoT devices", "Big data analytics"]  # CS de olsun ama az olsun
}

# 2. Prompt Şablonları (AI hep aynı giriş cümlesini kurmasın diye çeşitlendiriyoruz)
prompt_templates = [
    "Write an academic abstract about {topic}. The abstract should be between 150-250 words.",
    "Summarize the key concepts of {topic} in a formal academic tone. Limit to 200 words.",
    "Draft a research paper abstract investigating {topic}. Use scholarly language.",
    "Compose a scientific summary regarding {topic} for a university journal.",
    "Provide a comprehensive abstract analyzing {topic}."
]

# 3. Listeyi Oluştur
new_prompts = []

# Hedef: 1000 veri (Her konudan eşit sayıda)
target_count = 1000
count_per_topic = target_count // len(topics)  # Konu başına ~100 prompt

for category, subtopics in topics.items():
    for _ in range(count_per_topic):
        # Rastgele bir alt konu ve şablon seç
        topic = random.choice(subtopics)
        template = random.choice(prompt_templates)
        
        # Promptu oluştur
        prompt_text = template.format(topic=topic)
        new_prompts.append({
            "category": category,
            "topic": topic,
            "prompt": prompt_text
        })

# Kalan sayıyı rastgele dağıt
remaining = target_count - len(new_prompts)
for _ in range(remaining):
    category = random.choice(list(topics.keys()))
    topic = random.choice(topics[category])
    template = random.choice(prompt_templates)
    prompt_text = template.format(topic=topic)
    new_prompts.append({
        "category": category,
        "topic": topic,
        "prompt": prompt_text
    })

# 4. CSV Olarak Kaydet
prompt_df = pd.DataFrame(new_prompts)
output_path = "../Data/raw/diverse_prompts.csv"
prompt_df.to_csv(output_path, index=False, encoding='utf-8')

print(f"✓ Toplam {len(prompt_df)} adet çeşitli prompt oluşturuldu.")
print(f"✓ Kaydedildi: {output_path}")
print("\nKonu Dağılımı:")
print(prompt_df['category'].value_counts())
print("\nÖrnek Promptlar:")
for i, row in prompt_df.head(5).iterrows():
    print(f"{i+1}. [{row['category']}] {row['prompt']}")

