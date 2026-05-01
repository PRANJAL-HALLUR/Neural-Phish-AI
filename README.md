# NeuralPhish AI 🛡️

## Project Overview
NeuralPhish AI is an advanced machine learning-powered system designed to detect phishing attempts across URLs and SMS messages. With a modern, futuristic UI and a high-performance backend, it provides real-time analysis, confidence scores, and detailed explanations for its predictions.

## Problem Statement
Phishing attacks are becoming increasingly sophisticated, tricking users into revealing sensitive information through fraudulent links and text messages. Traditional rule-based filters struggle to keep up with these evolving threats. NeuralPhish AI addresses this by leveraging machine learning models trained on large datasets to accurately classify malicious content based on structural flags, lexical features, and contextual patterns.

## Features
- **URL Phishing Detection**: Analyzes URL structure, lexical features, and keywords to identify malicious links.
- **SMS Phishing Detection**: Uses Natural Language Processing (NLP) to detect fraudulent patterns in text messages.
- **Confidence Score & Risk Level**: Provides a percentage-based confidence score and categorizes risk as Low, Medium, or High.
- **Explanation Output**: Offers detailed reasoning for the classification, including structural flags and detected keywords.
- **Modern User Interface**: A sleek, dark-themed React frontend with real-time feedback and history tracking.

## Tech Stack
- **Frontend**: React, Vite, Framer Motion, Lucide React
- **Backend**: FastAPI, Uvicorn, Python
- **Machine Learning**: Scikit-Learn, Pandas, NLTK, Joblib
- **Deployment/Exposure**: ngrok (for exposing the local server to the web)

## Dataset Information
The models are trained on robust datasets to ensure high accuracy:
- **URL Dataset**: A comprehensive collection of benign and malicious URLs, evaluating features like URL length, domain characteristics, special characters, and keyword presence.
- **SMS Dataset**: A dataset of spam and ham (legitimate) messages, preprocessed using NLTK for tokenization and vectorized using TF-IDF.

## Model Information
- **SMS Model**: Logistic Regression trained on TF-IDF features.
- **URL Model**: Random Forest Classifier trained on lexical and structural URL features.
Both models are serialized using `joblib` and are optimized for quick inference in a production environment.

## Installation Steps

### Prerequisites
- Python 3.9+
- Node.js (v18+)
- Git

### Clone the Repository
```bash
git clone <your-repository-url>
cd ai_model
```

### 1. Backend Setup
Navigate to the backend directory and install the requirements:
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
# Activate the virtual environment
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Frontend Setup
Navigate to the frontend directory and install the node modules:
```bash
cd frontend
npm install
```

### 3. Environment Configuration
Create a `.env` file in the `frontend` directory (you can copy from `.env.example`):
```bash
cp .env.example .env
```
Ensure `VITE_API_BASE_URL` points to your backend (or ngrok URL).

## How to Run

### Run Backend
From the root directory (`ai_model`), start the FastAPI server:
```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be accessible at `http://localhost:8000`.

### Run Frontend
Open a new terminal, navigate to the frontend directory, and start the development server:
```bash
cd frontend
npm run dev
```
The UI will be accessible at `http://localhost:5173`.

### Run Ngrok (Optional for Public Access)
To expose your local backend to the internet, install ngrok and run:
```bash
ngrok http 8000
```
Update your frontend `.env` file with the generated ngrok URL (e.g., `VITE_API_BASE_URL=https://<your-ngrok-id>.ngrok-free.dev/predict`).

## API Endpoints

### 1. `POST /predict/message`
- **Description**: Predicts if an SMS message is phishing.
- **Body**: `{"text": "Your message here"}`
- **Response**:
```json
{
  "prediction": "Phishing",
  "confidence": 85.5,
  "risk_level": "High Risk 🚨",
  "reason": "Suspicious keyword detected",
  "keywords_detected": ["urgent", "verify"]
}
```

### 2. `POST /predict/url`
- **Description**: Predicts if a URL is phishing.
- **Body**: `{"url": "http://suspicious-link.com"}`
- **Response**:
```json
{
  "prediction": "Suspicious",
  "confidence": 65.0,
  "risk_level": "Medium Risk ⚠️",
  "reason": "Suspicious URL structure",
  "domain_status": "Unknown",
  "structural_flags": ["High hyphen count (3)"]
}
```

## Screenshots
> *(Add screenshots of your application here)*

- **Home Dashboard:**
  ![Home Dashboard Placeholder](#)
- **URL Detection Result:**
  ![URL Result Placeholder](#)
- **SMS Detection Result:**
  ![SMS Result Placeholder](#)

## Future Scope
- **Browser Extension**: Develop a Chrome/Firefox extension for real-time URL scanning.
- **Deep Learning Models**: Integrate LSTM or BERT models for improved NLP context understanding.
- **User Authentication**: Allow users to save their scan history securely.
- **API Rate Limiting**: Implement advanced security measures for the backend API.

## Contributors
- **[Your Name/Team Name]** - *Initial Work & Development*
