# NeuralPhish AI 🛡️

NeuralPhish AI is an advanced machine learning-powered system designed to detect phishing attempts across URLs and SMS messages. Featuring a modern, cyber-defense styled React frontend and a robust FastAPI backend, it provides real-time threat analysis, confidence scores, risk level breakdowns, and explainable AI insights.

---

## 🚀 Key Improvements & Architecture

- **Single-Service Architecture**: In production, the FastAPI server serves both the built React Single-Page Application (SPA) at `GET /` and the prediction APIs (`POST /predict/message`, `POST /predict/url`) under a unified host and port.
- **No More Root 404s**: The root URL `GET /` directly delivers the React UI. Direct browser refreshes on SPA routes are handled with seamless fallback to `index.html`.
- **API Segregation**: Unmatched API endpoints (`/predict/*`, `/api/*`) return clean JSON 404 responses instead of returning HTML.
- **One-Command Local Startup**: Launch the entire application on Windows with a single click using `run_project.bat`.
- **Zero Hardcoded URLs**: Frontend uses relative API paths (`/predict/message`, `/predict/url`) in production and transparent Vite dev-server proxying in development mode.
- **Cloud-Ready for Render**: Includes `render.yaml` and `build.sh` for instant, one-click single-service deployment without ngrok.
- **Robust Model Loading**: Serialized joblib models are resolved relative to source files and include scikit-learn version-compatibility safeguards.

---

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Framer Motion, Lucide React, Modern Cyber-Themed CSS
- **Backend**: FastAPI, Uvicorn, Python 3.10+
- **Machine Learning**: Scikit-Learn (Logistic Regression & Random Forest), Pandas, NLTK, Joblib
- **Deployment**: Render (Single Web Service), Docker/Linux compatible

---

## 🧠 Machine Learning Models

1. **SMS Phishing Detection**:
   - **Model**: Logistic Regression
   - **Features**: TF-IDF N-gram vectorizer with NLTK tokenization and text preprocessing.
   - **Heuristics**: Keyword pattern boosting for high-urgency terms (`urgent`, `verify`, `account`, `win`, `prize`).
   - **Artifacts**: `models/sms_model.pkl`, `models/vectorizer.pkl`

2. **URL Phishing Detection**:
   - **Model**: Random Forest Classifier (200 estimators)
   - **Features**: 10 structural & lexical URL features (`url_length`, `num_dots`, `has_https`, `special_chars`, `domain_length`, `subdomain_count`, `has_ip`, `hyphen_count`, `digit_count`, `has_suspicious_word`).
   - **Heuristics**: Whitelisted domain recognition (`google.com`, `amazon.in`, `github.com`, etc.) and protocol bias checks.
   - **Artifacts**: `models/url_model.pkl`

---

## ⚡ Quick Start (Local Development)

### Prerequisites
- **Python 3.10+**
- **Node.js v18+** & **npm**

### Option A: One-Command Startup (Windows)
Double-click `run_project.bat` or run in terminal:
```cmd
run_project.bat
```
This launcher checks dependencies, starts the FastAPI backend on `http://127.0.0.1:8000`, starts the Vite frontend on `http://localhost:5173`, and opens the interfaces.

### Option B: Manual Local Startup

**1. Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

**2. Install Frontend Dependencies:**
```bash
cd frontend
npm install
cd ..
```

**3. Run FastAPI Backend:**
```bash
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Docs: `http://localhost:8000/docs`

**4. Run Vite Frontend (Separate Terminal):**
```bash
cd frontend
npm run dev
```
- Frontend UI: `http://localhost:5173`
- *Note: Vite automatically proxies API calls from `http://localhost:5173/predict/*` to `http://localhost:8000/predict/*`.*

### Option C: Single-Service Production Preview
To preview how the application runs in production (single server serving frontend + API):
```bash
# 1. Build frontend
cd frontend
npm run build
cd ..

# 2. Run unified server
python run.py
```
- Open `http://localhost:8000` to see the full application.

---

## ☁️ Deployment Guide (Render - Single Web Service)

Deploy the entire application as a single web service on Render without ngrok.

### Step-by-Step Instructions:

1. **Push your repository to GitHub / GitLab.**
2. Log into the [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** > **Web Service**.
4. Connect your repository.
5. Configure the service:
   - **Name**: `neuralphish-ai`
   - **Runtime**: `Python 3`
   - **Region**: Any (e.g. `Oregon (US West)`)
   - **Branch**: `main`
   - **Build Command**:
     ```bash
     ./build.sh
     ```
     *(Alternatively: `pip install -r requirements.txt && npm --prefix frontend install && npm --prefix frontend run build`)*
   - **Start Command**:
     ```bash
     uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: `Free`
6. Click **Deploy Web Service**.
7. Once deployed, open your Render URL (e.g., `https://neuralphish-ai.onrender.com`).
   - The React homepage opens immediately at `/`.
   - The interactive Swagger docs are live at `/docs`.
   - Threat predictions work seamlessly from the UI.

---

## 📡 API Endpoints

### 1. `POST /predict/message`
Analyzes text or SMS messages for phishing and fraudulent patterns.

- **Request Body**:
```json
{
  "text": "URGENT: Your bank account has been suspended! Click here to verify: http://secure-login.com"
}
```

- **Response (200 OK)**:
```json
{
  "prediction": "Phishing",
  "confidence": 60.0,
  "risk_level": "Medium",
  "reason": "Suspicious keyword detected",
  "keywords_detected": ["urgent", "verify", "account", "click"]
}
```

### 2. `POST /predict/url`
Analyzes URLs for structural abnormalities, keyword impersonation, and phishing signatures.

- **Request Body**:
```json
{
  "url": "http://paypal-verification-account.com"
}
```

- **Response (200 OK)**:
```json
{
  "prediction": "Phishing",
  "confidence": 100.0,
  "risk_level": "High",
  "reason": "Phishing keywords in URL",
  "domain_status": "Unknown",
  "structural_flags": [
    "Suspicious words in URL",
    "High hyphen count (3)",
    "Missing HTTPS protocol"
  ]
}
```

### 3. `GET /api/health`
Health check for uptime monitors.
```json
{
  "status": "healthy",
  "service": "NeuralPhish AI",
  "frontend_built": true
}
```

### 4. `GET /docs`
FastAPI interactive Swagger UI for testing API endpoints.

---

## 🔒 Security & Best Practices

- Model binaries are bundled for fast zero-retraining inference.
- Heavy training CSV datasets (`url_dataset.csv` ~56MB) are excluded via `.gitignore` to keep repository size lean and deploys fast.
- Sensitive environment variables, local virtualenvs, and ngrok binaries are strictly ignored.
