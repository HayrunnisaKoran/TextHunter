"""
ML Model Eğitim Scripti
- 3 farklı ML algoritması ile model eğitimi
- Naive Bayes, Random Forest, SVM
- Model kaydetme ve metrik hesaplama
"""

import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# NLTK verilerini indir (ilk çalıştırmada)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

INPUT_DIR = "../Data/cleaned"
OUTPUT_DIR = "../MLModels"

# Türkçe ve İngilizce stopwords
try:
    stop_words_en = set(stopwords.words('english'))
    stop_words_tr = set(stopwords.words('turkish'))
    stop_words = stop_words_en.union(stop_words_tr)
except:
    stop_words = set(stopwords.words('english'))

def load_data():
    """
    Temizlenmiş veri setini yükler
    """
    json_path = os.path.join(INPUT_DIR, "cleaned_dataset.json")
    csv_path = os.path.join(INPUT_DIR, "cleaned_dataset.csv")
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path, encoding='utf-8')
        data = df.to_dict('records')
    else:
        raise FileNotFoundError("Temizlenmiş veri seti bulunamadı. Önce veri temizleme scriptini çalıştırın.")
    
    df = pd.DataFrame(data)
    return df['text'].values, df['label'].values

def train_naive_bayes(X_train, X_test, y_train, y_test, vectorizer_type='bow'):
    """
    Naive Bayes modeli eğitir
    """
    print(f"\n{'='*60}")
    print(f"Naive Bayes ({vectorizer_type.upper()}) Eğitiliyor...")
    print(f"{'='*60}")
    
    # Vectorizer seçimi
    if vectorizer_type == 'bow':
        vectorizer = CountVectorizer(max_features=5000, stop_words=list(stop_words))
    else:  # tfidf
        vectorizer = TfidfVectorizer(max_features=5000, stop_words=list(stop_words))
    
    # Özellik çıkarımı
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Model eğitimi
    model = MultinomialNB(alpha=1.0)
    model.fit(X_train_vec, y_train)
    
    # Tahmin ve metrikler
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print(f"\nConfusion Matrix:\n{cm}")
    
    # Model ve vectorizer'ı kaydet
    model_name = f"naive_bayes_{vectorizer_type}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    joblib.dump(model, os.path.join(OUTPUT_DIR, f"{model_name}_model.pkl"))
    joblib.dump(vectorizer, os.path.join(OUTPUT_DIR, f"{model_name}_vectorizer.pkl"))
    
    return {
        'model_name': model_name,
        'model': model,
        'vectorizer': vectorizer,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist()
    }

def train_random_forest(X_train, X_test, y_train, y_test, vectorizer_type='bow'):
    """
    Random Forest modeli eğitir
    """
    print(f"\n{'='*60}")
    print(f"Random Forest ({vectorizer_type.upper()}) Eğitiliyor...")
    print(f"{'='*60}")
    
    # Vectorizer seçimi
    if vectorizer_type == 'bow':
        vectorizer = CountVectorizer(max_features=5000, stop_words=list(stop_words))
    else:  # tfidf
        vectorizer = TfidfVectorizer(max_features=5000, stop_words=list(stop_words))
    
    # Özellik çıkarımı
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Model eğitimi
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_vec, y_train)
    
    # Tahmin ve metrikler
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print(f"\nConfusion Matrix:\n{cm}")
    
    # Model ve vectorizer'ı kaydet
    model_name = f"random_forest_{vectorizer_type}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    joblib.dump(model, os.path.join(OUTPUT_DIR, f"{model_name}_model.pkl"))
    joblib.dump(vectorizer, os.path.join(OUTPUT_DIR, f"{model_name}_vectorizer.pkl"))
    
    return {
        'model_name': model_name,
        'model': model,
        'vectorizer': vectorizer,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist()
    }

def train_svm(X_train, X_test, y_train, y_test, vectorizer_type='bow'):
    """
    SVM modeli eğitir
    """
    print(f"\n{'='*60}")
    print(f"SVM ({vectorizer_type.upper()}) Eğitiliyor...")
    print(f"{'='*60}")
    
    # Vectorizer seçimi
    if vectorizer_type == 'bow':
        vectorizer = CountVectorizer(max_features=5000, stop_words=list(stop_words))
    else:  # tfidf
        vectorizer = TfidfVectorizer(max_features=5000, stop_words=list(stop_words))
    
    # Özellik çıkarımı
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Model eğitimi (SVM için daha küçük örneklem kullanılabilir)
    model = SVC(kernel='linear', probability=True, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Tahmin ve metrikler
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print(f"\nConfusion Matrix:\n{cm}")
    
    # Model ve vectorizer'ı kaydet
    model_name = f"svm_{vectorizer_type}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    joblib.dump(model, os.path.join(OUTPUT_DIR, f"{model_name}_model.pkl"))
    joblib.dump(vectorizer, os.path.join(OUTPUT_DIR, f"{model_name}_vectorizer.pkl"))
    
    return {
        'model_name': model_name,
        'model': model,
        'vectorizer': vectorizer,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist()
    }

def main():
    """
    Ana fonksiyon - Tüm modelleri eğitir
    """
    print("=" * 60)
    print("ML MODEL EĞİTİMİ BAŞLATILIYOR")
    print("=" * 60)
    
    # Veriyi yükle
    X, y = load_data()
    print(f"\nYüklenen veri sayısı: {len(X)}")
    print(f"Sınıf dağılımı: {pd.Series(y).value_counts().to_dict()}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nEğitim seti: {len(X_train)} örnek")
    print(f"Test seti: {len(X_test)} örnek")
    
    # Model sonuçlarını sakla
    results = []
    
    # 1. Naive Bayes (BoW)
    results.append(train_naive_bayes(X_train, X_test, y_train, y_test, 'bow'))
    
    # 2. Naive Bayes (TF-IDF)
    results.append(train_naive_bayes(X_train, X_test, y_train, y_test, 'tfidf'))
    
    # 3. Random Forest (BoW)
    results.append(train_random_forest(X_train, X_test, y_train, y_test, 'bow'))
    
    # 4. Random Forest (TF-IDF)
    results.append(train_random_forest(X_train, X_test, y_train, y_test, 'tfidf'))
    
    # 5. SVM (BoW)
    results.append(train_svm(X_train, X_test, y_train, y_test, 'bow'))
    
    # 6. SVM (TF-IDF)
    results.append(train_svm(X_train, X_test, y_train, y_test, 'tfidf'))
    
    # Sonuçları kaydet
    results_summary = []
    for result in results:
        results_summary.append({
            'model_name': result['model_name'],
            'accuracy': float(result['accuracy']),
            'precision': float(result['precision']),
            'recall': float(result['recall']),
            'f1_score': float(result['f1_score']),
            'confusion_matrix': result['confusion_matrix']
        })
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "training_results.json"), 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, ensure_ascii=False, indent=2)
    
    # Özet
    print("\n" + "=" * 60)
    print("EĞİTİM ÖZETİ")
    print("=" * 60)
    for result in results_summary:
        print(f"{result['model_name']:30s} - Accuracy: {result['accuracy']:.4f}, F1: {result['f1_score']:.4f}")
    
    print(f"\nModeller kaydedildi: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

