import sys
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

# Ensure project root is in sys.path so 'src' can always be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.predict import predict_message, predict_url

logger = logging.getLogger("neuralphish")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"

app = FastAPI(
    title="NeuralPhish AI API",
    description="API for predicting if SMS messages or URLs are phishing.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    text: str = Field(..., min_length=1, description="SMS text content to analyze")

class UrlRequest(BaseModel):
    url: str = Field(..., min_length=1, description="URL string to analyze")

def format_response(result: dict) -> dict:
    confidence = result.get("confidence", 0.0)
    
    if confidence < 40.0:
        prediction_str = "Safe"
        risk = "Low"
    elif confidence <= 70.0:
        prediction_str = "Suspicious"
        risk = "Medium"
    else:
        prediction_str = "Phishing"
        risk = "High"
        
    formatted = {
        "prediction": prediction_str,
        "confidence": confidence,
        "risk_level": risk,
        "reason": result.get("reason", "Unknown")
    }
    
    if "domain_status" in result:
        formatted["domain_status"] = result["domain_status"]
    if "structural_flags" in result:
        formatted["structural_flags"] = result["structural_flags"]
    if "keywords_detected" in result:
        formatted["keywords_detected"] = result["keywords_detected"]
        
    return formatted

# --- API Endpoints ---

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring and uptime verification."""
    return {
        "status": "healthy",
        "service": "NeuralPhish AI",
        "frontend_built": (FRONTEND_DIST / "index.html").is_file()
    }

@app.post("/predict/message")
async def api_predict_message(req: MessageRequest):
    cleaned = req.text.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        res = predict_message(cleaned)
        return format_response(res)
    except Exception as e:
        logger.error(f"Error predicting message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while analyzing the message. Please try again.")

@app.post("/predict/url")
async def api_predict_url(req: UrlRequest):
    cleaned = req.url.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Input URL cannot be empty.")
    try:
        res = predict_url(cleaned)
        return format_response(res)
    except Exception as e:
        logger.error(f"Error predicting URL: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while analyzing the URL. Please try again.")

# --- Static Files and Frontend Single-Service Serving ---

# Mount assets directory if available
assets_dir = FRONTEND_DIST / "assets"
if assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

@app.get("/", include_in_schema=False)
async def serve_root():
    """Serve the frontend single-page application at the root URL."""
    index_file = FRONTEND_DIST / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file))
    return JSONResponse(
        status_code=200,
        content={
            "status": "online",
            "message": "NeuralPhish AI API is running.",
            "note": "Frontend production build not found at 'frontend/dist'. Run 'npm run build' inside 'frontend' for single-service deployment, or use the Vite dev server at http://localhost:5173.",
            "docs": "/docs",
            "endpoints": {
                "predict_message": "POST /predict/message",
                "predict_url": "POST /predict/url",
                "health": "GET /api/health"
            }
        }
    )

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend_spa(full_path: str):
    """
    Catch-all route:
    - Returns JSON 404 for unknown API or docs paths
    - Serves static files if they exist in frontend/dist (e.g. favicon.svg)
    - Fallbacks to index.html for React SPA client routes
    """
    api_prefixes = ("predict/", "api/", "docs", "redoc", "openapi.json")
    if any(full_path.startswith(prefix) or full_path == prefix for prefix in api_prefixes):
        raise HTTPException(status_code=404, detail=f"API endpoint '/{full_path}' not found.")

    # Check if a static file directly exists in FRONTEND_DIST (e.g. favicon.svg, icons.svg)
    requested_file = FRONTEND_DIST / full_path
    if requested_file.is_file():
        return FileResponse(str(requested_file))

    # Fallback to index.html for client-side routing
    index_file = FRONTEND_DIST / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file))

    raise HTTPException(
        status_code=404,
        detail="Resource not found and frontend production build is missing. Run 'npm run build' inside 'frontend'."
    )
