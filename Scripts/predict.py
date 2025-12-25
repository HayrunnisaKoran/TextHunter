"""
Python Model Tahmin Scripti
C# uygulamasından çağrılacak tahmin scripti
"""

import sys
import json
import os
import joblib
import numpy as np


# Model dizini - Script'in bulunduğu dizinden yola çıkarak MLModels klasörünü bul
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Scripts/ klasöründen bir üst dizin (proje root)
MODEL_DIR = os.path.join(PROJECT_ROOT, "MLModels")

def load_model(model_name):
    mapping = {"svm_model": "svm_model.pkl", "logistic_regression": "logistic_regression.pkl", "naive_bayes": "naive_bayes.pkl"}
    file_name = mapping.get(model_name, f"{model_name}.pkl")
    model_path = os.path.join(MODEL_DIR, file_name)
    vectorizer_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
    
    if not os.path.exists(model_path): return None, None
    return joblib.load(model_path), joblib.load(vectorizer_path)
  
    
   
def predict_text(text, model_name):
    model, vectorizer = load_model(model_name)
    if not model: return None
    
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    prediction = str(prediction.item() if hasattr(prediction, "item") else prediction)
    
    try:
        probs = model.predict_proba(text_vec)[0]
        # Ham rakamları (0 ve 1) anahtar olarak gönderiyoruz, C# bunları eşleştirecek
        prob_dict = {str(cls): float(p) for cls, p in zip(model.classes_, probs)}
    except:
        prob_dict = {prediction: 1.0}

    return {'prediction': prediction, 'probabilities': prob_dict}
   

def predict_multiple_models(text):
    """
    Birden fazla model ile tahmin yapar (Tüm 6 model)
    """
    # Kullanılacak tüm modeller (6 model) 
    models = [
        'naive_bayes',
        'logistic_regression',
        'svm_model'
    ]
    
    results = {}
    
    for model_name in models:
        result = predict_text(text, model_name)
        if result:
            results[model_name] = result
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    results = {}
    for m in ['naive_bayes', 'logistic_regression', 'svm_model']:
        res = predict_text(sys.argv[1], m)
        if res: results[m] = res
    print(json.dumps(results))

