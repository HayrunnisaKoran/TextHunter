"""
Python Model Tahmin Scripti
C# uygulamasından çağrılacak tahmin scripti
"""

import sys
import json
import os
import joblib
import numpy as np

# Model dizini
MODEL_DIR = "../MLModels"

def load_model(model_name):
    """
    Model ve vectorizer'ı yükler
    """
    model_path = os.path.join(MODEL_DIR, f"{model_name}_model.pkl")
    vectorizer_path = os.path.join(MODEL_DIR, f"{model_name}_vectorizer.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return None, None
    
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    return model, vectorizer

def predict_text(text, model_name):
    """
    Tek bir metin için tahmin yapar
    """
    model, vectorizer = load_model(model_name)
    
    if model is None or vectorizer is None:
        return None
    
    # Metni vectorize et
    text_vec = vectorizer.transform([text])
    
    # Tahmin yap
    prediction = model.predict(text_vec)[0]
    
    # Olasılıkları al (eğer model destekliyorsa)
    try:
        probabilities = model.predict_proba(text_vec)[0]
        prob_dict = dict(zip(model.classes_, probabilities))
    except:
        prob_dict = {prediction: 1.0}
    
    return {
        'prediction': prediction,
        'probabilities': prob_dict
    }

def predict_multiple_models(text):
    """
    Birden fazla model ile tahmin yapar (Tüm 6 model)
    """
    # Kullanılacak tüm modeller (6 model)
    models = [
        'naive_bayes_bow',
        'naive_bayes_tfidf',
        'random_forest_bow',
        'random_forest_tfidf',
        'svm_bow',
        'svm_tfidf'
    ]
    
    results = {}
    
    for model_name in models:
        result = predict_text(text, model_name)
        if result:
            results[model_name] = result
    
    return results

if __name__ == "__main__":
    # Komut satırından metin al
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Metin parametresi gerekli"}))
        sys.exit(1)
    
    text = sys.argv[1]
    
    # Birden fazla model ile tahmin yap
    results = predict_multiple_models(text)
    
    # JSON olarak çıktı ver
    print(json.dumps(results, ensure_ascii=False))

