from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import time
import logging
import os
from typing import List, Optional

LOG = logging.getLogger("mlserve")
logging.basicConfig(level=logging.INFO)

MODEL = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

def load_model(path: str) -> Optional[object]:
    try:
        m = joblib.load(path)
        LOG.info("Loaded model from %s", path)
        return m
    except Exception as e:
        LOG.warning("Failed to load model at %s: %s", path, e)
        return None


MODEL = load_model(MODEL_PATH)

app = FastAPI(title="Fake WiFi Detector ML")

# Allow any origin for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "OK", "model_loaded": MODEL is not None, "timestamp": time.time()}


@app.post("/scan")
async def scan_data(request: Request):
    data = await request.json()
    LOG.info("[SCAN] Received data: %s", data)
    # Echo back for compatibility; clients should use /predict for ML
    return {"status": "received", "data": data}


class WifiScan(BaseModel):
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    signal: Optional[int] = None
    channel: Optional[int] = None
    security: Optional[str] = None
    vendor: Optional[str] = None


class Scan(BaseModel):
    agent_id: str
    timestamp: float
    scans: List[WifiScan]


@app.post("/predict")
def predict(scan: Scan):
    # If model not available, return safe defaults and an explanatory message
    if MODEL is None:
        LOG.warning("Predict called but no model loaded. Returning defaults.")
        out = []
        for s in scan.scans:
            out.append({
                "ssid": s.ssid,
                "bssid": s.bssid,
                "signal": s.signal,
                "channel": s.channel,
                "security": s.security,
                "vendor": s.vendor,
                "is_fake": False,
                "confidence": 0.0,
            })
        return {"detections": out, "model_loaded": False, "message": "No model available; please run train.py to create model.pkl"}

    feats = []
    for s in scan.scans:
        signal = s.signal if isinstance(s.signal, int) else -80
        channel = int(s.channel) if s.channel and str(s.channel).isdigit() else 1
        security = s.security or 'OPEN'
        vendor = s.vendor or 'None'
        ssid = s.ssid or ''
        ssid_len = len(ssid)
        ssid_special = int(any(c in ssid for c in ['_','-','@']))

        feats.append({
            'signal': signal,
            'channel': channel,
            'security': security,
            'vendor': vendor,
            'ssid_len': ssid_len,
            'ssid_has_special': ssid_special,
        })

    df = pd.DataFrame(feats)
    try:
        proba = MODEL.predict_proba(df)[:, 1]
        preds = (proba > 0.5).astype(int).tolist()
    except Exception as e:
        LOG.error("Model predict failed: %s", e)
        
        # fallback to safe defaults
        proba = [0.0] * len(feats)
        preds = [0] * len(feats)

    out = []
    for p, pb, orig in zip(preds, proba, scan.scans):
        det = {
            'ssid': orig.ssid,
            'bssid': orig.bssid,
            'signal': orig.signal,
            'channel': orig.channel,
            'security': orig.security,
            'vendor': orig.vendor,
            'is_fake': bool(int(p)),
            'confidence': round(float(pb), 3),
        }
        out.append(det)

    return {'detections': out, 'model_loaded': True}


if __name__ == "__main__":
    LOG.info("Starting ML service (uvicorn)... model_loaded=%s", MODEL is not None)
    uvicorn.run("serve:app", host="0.0.0.0", port=8000, reload=False)
