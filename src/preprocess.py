import os
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse

# Download NLTK resources safely
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception:
    pass

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    try:
        stop_words = set(stopwords.words('english'))
    except Exception:
        stop_words = set()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

def extract_url_features(url_series):
    features = []
    suspicious_keywords = ['login', 'verify', 'update', 'bank', 'secure', 'account', 'paypal', 'signin', 'confirm']
    
    for url in url_series:
        if not isinstance(url, str):
            url = ""
        
        domain = ""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc if parsed.netloc else parsed.path.split('/')[0]
        except:
            pass
            
        features.append({
            'url_length': len(url),
            'num_dots': url.count('.'),
            'has_https': 1 if url.startswith('https://') else 0,
            'special_chars': url.count('@') + url.count('-') + url.count('//'),
            'domain_length': len(domain),
            'subdomain_count': domain.count('.'),
            'has_ip': 1 if any(char.isdigit() for char in domain) else 0,
            'hyphen_count': url.count('-'),
            'digit_count': sum(char.isdigit() for char in url),
            'has_suspicious_word': 1 if any(keyword in url.lower() for keyword in suspicious_keywords) else 0
        })
        
    df_features = pd.DataFrame(features)
    
    # FINAL FEATURE ORDER (MUST MATCH)
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
    return df_features[feature_order]

def preprocess_sms_data(filepath):
    df = pd.read_csv(filepath, encoding='latin-1')
    
    # Columns v1 -> label, v2 -> message
    if 'v1' in df.columns and 'v2' in df.columns:
        df = df[['v1', 'v2']].copy()
        df.columns = ['label', 'message']
    else:
        df = df.iloc[:, [0, 1]].copy()
        df.columns = ['label', 'message']

    df['label'] = df['label'].astype(str).str.lower().map({'spam': 1, 'ham': 0})
    df.dropna(subset=['label', 'message'], inplace=True)
    df['label'] = df['label'].astype(int)

    df['clean_text'] = df['message'].apply(clean_text)
    return df

def preprocess_url_data(filepath):
    df = pd.read_csv(filepath, encoding='latin-1')

    # Auto-detect columns: specifically prioritize the 'URL' column over filename indices
    url_col = next((c for c in df.columns if c.lower() == 'url'), df.columns[0])
    label_col = df.columns[-1]
    
    df.rename(columns={url_col: 'url', label_col: 'label'}, inplace=True)
    df = df[['url', 'label']].copy()
    
    df.dropna(subset=['url', 'label'], inplace=True)
    
    if df['label'].dtype == object:
         df['label'] = df['label'].astype(str).str.lower().map({'phishing': 1, 'safe': 0, 'bad': 1, 'good': 0})
         df.dropna(subset=['label'], inplace=True)
         
    df['label'] = df['label'].astype(int)
    
    # Fix dataset label issue if inverted
    if df['label'].mean() >= 0.5:
        df['label'] = 1 - df['label']

    features = extract_url_features(df['url'])
    return pd.concat([features, df['label'].reset_index(drop=True)], axis=1)