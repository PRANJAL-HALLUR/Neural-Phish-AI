"""
NeuralPhish AI - Full Automated Verification Suite
Tests the FastAPI backend, model inference, SPA routing, static files, and error handling.
"""
import sys
import os
from pathlib import Path

# Set stdout to UTF-8 for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Set up project root
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Test model files existence
print("=" * 60)
print("TEST 1: Model Files Verification")
print("=" * 60)
models_dir = PROJECT_ROOT / "models"
sms_path = models_dir / "sms_model.pkl"
url_path = models_dir / "url_model.pkl"
vec_path = models_dir / "vectorizer.pkl"

assert sms_path.is_file(), f"Missing sms_model.pkl at {sms_path}"
assert url_path.is_file(), f"Missing url_model.pkl at {url_path}"
assert vec_path.is_file(), f"Missing vectorizer.pkl at {vec_path}"
print(f"[PASS] sms_model.pkl found ({sms_path.stat().st_size} bytes)")
print(f"[PASS] url_model.pkl found ({url_path.stat().st_size} bytes)")
print(f"[PASS] vectorizer.pkl found ({vec_path.stat().st_size} bytes)")

# Test frontend build existence
print("\n" + "=" * 60)
print("TEST 2: Frontend Production Build Verification")
print("=" * 60)
dist_dir = PROJECT_ROOT / "frontend" / "dist"
index_file = dist_dir / "index.html"
assets_dir = dist_dir / "assets"

assert index_file.is_file(), f"Missing index.html at {index_file}"
assert assets_dir.is_dir(), f"Missing assets directory at {assets_dir}"
css_files = list(assets_dir.glob("*.css"))
js_files = list(assets_dir.glob("*.js"))
assert len(css_files) > 0, "No CSS files found in assets"
assert len(js_files) > 0, "No JS files found in assets"
print(f"[PASS] frontend/dist/index.html found ({index_file.stat().st_size} bytes)")
print(f"[PASS] frontend/dist/assets found with {len(css_files)} CSS and {len(js_files)} JS bundles")

# Test ML predictions directly
print("\n" + "=" * 60)
print("TEST 3: Machine Learning Inference Functions")
print("=" * 60)
from src.predict import predict_message, predict_url

sms_res = predict_message("URGENT: Your account has been compromised. Click to verify your details.")
print(f"[PASS] predict_message: {sms_res}")
assert "prediction" in sms_res and "confidence" in sms_res and "risk_level" in sms_res
assert sms_res["prediction"] in (0, 1)

url_res = predict_url("http://paypal-verification-account.com")
print(f"[PASS] predict_url (phishing): {url_res}")
assert "prediction" in url_res and "confidence" in url_res and "risk_level" in url_res
assert url_res["prediction"] in (0, 1)

url_safe = predict_url("https://google.com")
print(f"[PASS] predict_url (safe): {url_safe}")
assert url_safe["prediction"] == 0

# Test FastAPI endpoints via TestClient
print("\n" + "=" * 60)
print("TEST 4: FastAPI Application Endpoints & Routing")
print("=" * 60)
from starlette.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

# 4.1 Homepage GET /
res = client.get("/")
print(f"GET / -> Status {res.status_code}")
assert res.status_code == 200, f"Expected 200 on /, got {res.status_code}"
assert "text/html" in res.headers.get("content-type", "")
assert "<!doctype html>" in res.text.lower() or "<html" in res.text.lower()
print("[PASS] GET / serves the React frontend HTML.")

# 4.2 GET /docs
res = client.get("/docs")
print(f"GET /docs -> Status {res.status_code}")
assert res.status_code == 200
assert "swagger" in res.text.lower() or "html" in res.headers.get("content-type", "")
print("[PASS] GET /docs serves Swagger UI documentation.")

# 4.3 GET /api/health
res = client.get("/api/health")
print(f"GET /api/health -> Status {res.status_code}, Body: {res.json()}")
assert res.status_code == 200
assert res.json().get("status") == "healthy"
print("[PASS] GET /api/health returns healthy status.")

# 4.4 POST /predict/message with valid body
res = client.post("/predict/message", json={"text": "URGENT: Claim your free prize now! Call 800-1234."})
print(f"POST /predict/message -> Status {res.status_code}, Body: {res.json()}")
assert res.status_code == 200
body = res.json()
assert "prediction" in body and "confidence" in body and "risk_level" in body
assert body["prediction"] in ("Safe", "Suspicious", "Phishing")
assert body["risk_level"] in ("Low", "Medium", "High")
print("[PASS] POST /predict/message handles valid request successfully.")

# 4.5 POST /predict/message with empty body
res = client.post("/predict/message", json={"text": "   "})
print(f"POST /predict/message (empty) -> Status {res.status_code}")
assert res.status_code == 400
assert "cannot be empty" in res.json().get("detail", "")
print("[PASS] POST /predict/message rejects empty input with 400.")

# 4.6 POST /predict/url with valid body
res = client.post("/predict/url", json={"url": "http://suspicious-banking-update.net/login"})
print(f"POST /predict/url -> Status {res.status_code}, Body: {res.json()}")
assert res.status_code == 200
body = res.json()
assert "prediction" in body and "confidence" in body and "risk_level" in body
assert body["prediction"] in ("Safe", "Suspicious", "Phishing")
print("[PASS] POST /predict/url handles valid request successfully.")

# 4.7 POST /predict/url with empty body
res = client.post("/predict/url", json={"url": "   "})
print(f"POST /predict/url (empty) -> Status {res.status_code}")
assert res.status_code == 400
assert "cannot be empty" in res.json().get("detail", "")
print("[PASS] POST /predict/url rejects empty input with 400.")

# 4.8 Unknown API endpoint returns JSON 404
res = client.get("/predict/nonexistent_route")
print(f"GET /predict/nonexistent_route -> Status {res.status_code}, Content-Type: {res.headers.get('content-type')}")
assert res.status_code == 404
assert "application/json" in res.headers.get("content-type", "")
assert "not found" in res.json().get("detail", "").lower()
print("[PASS] Unknown API routes return JSON 404 (not HTML).")

res = client.get("/api/unknown_endpoint")
print(f"GET /api/unknown_endpoint -> Status {res.status_code}, Content-Type: {res.headers.get('content-type')}")
assert res.status_code == 404
assert "application/json" in res.headers.get("content-type", "")
print("[PASS] Unknown /api/* routes return JSON 404.")

# 4.9 Direct browser refresh on SPA route returns index.html (HTTP 200)
res = client.get("/history")
print(f"GET /history (SPA client route) -> Status {res.status_code}")
assert res.status_code == 200
assert "text/html" in res.headers.get("content-type", "")
assert "<!doctype html>" in res.text.lower() or "<html" in res.text.lower()
print("[PASS] SPA client routes fallback to index.html with HTTP 200 on refresh.")

# 4.10 Static asset serving
css_rel = f"/assets/{css_files[0].name}"
res = client.get(css_rel)
print(f"GET {css_rel} -> Status {res.status_code}, Content-Type: {res.headers.get('content-type')}")
assert res.status_code == 200
assert "css" in res.headers.get("content-type", "")
print("[PASS] Static CSS assets load successfully.")

print("\n" + "=" * 60)
print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY! 100% OK")
print("=" * 60)
