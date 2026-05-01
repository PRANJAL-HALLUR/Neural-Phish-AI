import os
import joblib
import pandas as pd
from src.preprocess import clean_text, extract_url_features

def get_models_dir():
    # Attempt to locate models relative to this file
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    models_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(models_dir):
        # Fallback if run from different dir
        models_dir = os.path.join(os.getcwd(), 'models')
        
    return models_dir

# Lazily loaded cached models
_sms_model = None
_vectorizer = None
_url_model = None

def load_sms_model():
    global _sms_model, _vectorizer
    if _sms_model is None or _vectorizer is None:
        models_dir = get_models_dir()
        sms_model_path = os.path.join(models_dir, 'sms_model.pkl')
        vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
        _sms_model = joblib.load(sms_model_path)
        _vectorizer = joblib.load(vectorizer_path)
    return _sms_model, _vectorizer

def load_url_model():
    global _url_model
    if _url_model is None:
        models_dir = get_models_dir()
        url_model_path = os.path.join(models_dir, 'url_model.pkl')
        _url_model = joblib.load(url_model_path)
    return _url_model

def predict_message(text):
    """
    Predicts if an SMS message is phishing (1) or safe (0).
    Clean modular code suitable for backend integration.
    """
    if not isinstance(text, str):
        return {
            "prediction": 0,
            "confidence": 0.0,
            "risk_level": "Low Risk ✅",
            "reason": "Invalid input type"
        }
        
    text = text.strip().strip('"').strip("'")
    if not text:
        return {
            "prediction": 0,
            "confidence": 0.0,
            "risk_level": "Low Risk ✅",
            "reason": "Empty input"
        }
        
    model, vectorizer = load_sms_model()
    
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    
    prob = model.predict_proba(vectorized)[0][1]
    
    # Check for keywords
    keywords = ['urgent', 'alert', 'verify', 'update', 'account', 'win', 'prize', 'free', 'click']
    text_lower = text.lower()
    detected_keywords = [k for k in keywords if k in text_lower]
    keyword_flag = len(detected_keywords) > 0
    
    if keyword_flag:
        prob = max(prob, 0.6)
        reason = "Suspicious keyword detected"
    else:
        reason = "Based on message pattern"
        
    prediction = 1 if prob > 0.3 else 0
    confidence = round(prob * 100, 1)
    
    if prob > 0.8:
        risk = "High Risk 🚨"
    elif prob > 0.5:
        risk = "Medium Risk ⚠️"
    else:
        risk = "Low Risk ✅"
        
    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_level": risk,
        "reason": reason,
        "keywords_detected": detected_keywords
    }

def predict_url(url):
    """
    Predicts if a URL is phishing (1) or safe (0).
    Clean modular code suitable for backend integration.
    """
    if not isinstance(url, str):
        return {
            "prediction": 0,
            "confidence": 0.0,
            "risk_level": "Low Risk ✅",
            "reason": "Invalid input type"
        }
        
    url = url.strip().strip('"').strip("'")
    if not url:
        return {
            "prediction": 0,
            "confidence": 0.0,
            "risk_level": "Low Risk ✅",
            "reason": "Empty input"
        }
        
    trusted_domains = [
        "google.com",
        "flipkart.com",
        "amazon.in",
        "github.com",
        "openai.com"
    ]
    
    if any(domain in url.lower() for domain in trusted_domains):
        return {
            "prediction": 0,
            "confidence": 15.0,
            "risk_level": "Low Risk ✅",
            "reason": "Trusted domain",
            "domain_status": "Trusted",
            "structural_flags": []
        }
        
    model = load_url_model()
    
    # Extract features using SAME function as training
    raw_features_df = extract_url_features(pd.Series([url]))
    
    # Convert to DataFrame with EXACT same column order
    feature_order = [
         'url_length',
         'num_dots',
         'has_https',
         'special_chars',
         'domain_length',
         'subdomain_count',
         'has_ip',
         'hyphen_count',
         'digit_count',
         'has_suspicious_word'
    ]
    features_df = raw_features_df[feature_order].copy()
    
    prob = model.predict_proba(features_df)[0][1]
    
    # Structural bias heuristic targeting safe legitimate protocols handling false pos.
    if features_df['has_https'].iloc[0] == 1 and features_df['has_suspicious_word'].iloc[0] == 0:
        prob -= 0.5
        
    prob = max(0.0, min(1.0, prob))
    prediction = 1 if prob > 0.6 else 0
    
    confidence = round(prob * 100, 1)
    
    if prob > 0.8:
        risk = "High Risk 🚨"
    elif prob > 0.5:
        risk = "Medium Risk ⚠️"
    else:
        risk = "Low Risk ✅"
        
    if features_df['has_suspicious_word'].iloc[0] == 1:
        reason = "Phishing keywords in URL"
    elif features_df['hyphen_count'].iloc[0] >= 3 or features_df['digit_count'].iloc[0] >= 5:
        reason = "Suspicious URL structure"
    else:
        reason = "Based on URL pattern"
        
    structural_flags = []
    if features_df['has_suspicious_word'].iloc[0] == 1:
        structural_flags.append("Suspicious words in URL")
    if features_df['hyphen_count'].iloc[0] >= 3:
        structural_flags.append(f"High hyphen count ({features_df['hyphen_count'].iloc[0]})")
    if features_df['digit_count'].iloc[0] >= 5:
        structural_flags.append(f"High digit count ({features_df['digit_count'].iloc[0]})")
    if features_df['has_ip'].iloc[0] == 1:
        structural_flags.append("IP address used instead of domain")
    if features_df['has_https'].iloc[0] == 0:
        structural_flags.append("Missing HTTPS protocol")
        
    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_level": risk,
        "reason": reason,
        "domain_status": "Unknown",
        "structural_flags": structural_flags
    }
