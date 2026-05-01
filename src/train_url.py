import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from preprocess import preprocess_url_data

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    data_path = os.path.join(base_dir, 'data', 'url_dataset.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    df = preprocess_url_data(data_path)
    
    X = df.drop(columns=['label'])
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=15, random_state=42)
    model.fit(X_train, y_train)
    
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, 'url_model.pkl')
    joblib.dump(model, model_path)

if __name__ == '__main__':
    main()
