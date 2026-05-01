from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from src.predict import predict_message, predict_url

app = FastAPI(title="Phishing Detection API", description="API for predicting if SMS or URLs are phishing.")

# Configure CORS (allow all origins as requested)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    text: str = Field(..., min_length=1)

class UrlRequest(BaseModel):
    url: str = Field(..., min_length=1)

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

@app.post("/predict/message")
async def api_predict_message(req: MessageRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        res = predict_message(req.text)
        return format_response(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/url")
async def api_predict_url(req: UrlRequest):
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="Input URL cannot be empty.")
    try:
        res = predict_url(req.url)
        return format_response(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
