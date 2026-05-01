import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import preprocess_sms_data

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    data_path = os.path.join(base_dir, 'data', 'spam.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    df = preprocess_sms_data(data_path)
    X = df['clean_text']
    y = df['label']
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)
    
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(models_dir, 'vectorizer.pkl'))
    
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    model_path = os.path.join(models_dir, 'sms_model.pkl')
    joblib.dump(model, model_path)

if __name__ == '__main__':
    main()
