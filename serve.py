from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import joblib
import logging

from tensorflow.keras.models import load_model

# -------------------------
# Setup
# -------------------------
app = FastAPI(title="Wireless Threat Detection API")
logging.basicConfig(level=logging.INFO)

# -------------------------
# Load models
# -------------------------
autoencoder = load_model("models/autoencoder.h5")
classifier = load_model("models/cnn_bilstm.h5")
scaler = joblib.load("models/scaler.pkl")

# If you saved threshold during training, load it
# otherwise keep fixed
THRESHOLD = 0.05


# -------------------------
# Input schema
# -------------------------
class Traffic(BaseModel):
    features: List[float]


# -------------------------
# Health check
# -------------------------
@app.get("/health")
def health():
    return {"status": "running", "autoencoder_loaded": True, "classifier_loaded": True}


# -------------------------
# Main prediction endpoint
# -------------------------
@app.post("/predict")
def predict(data: Traffic):

    # -------------------------
    # Step 1: preprocessing
    # -------------------------
    X = np.array(data.features).reshape(1, -1)
    X_scaled = scaler.transform(X)

    # -------------------------
    # Step 2: Autoencoder (anomaly detection)
    # -------------------------
    reconstructed = autoencoder.predict(X_scaled)

    error = np.mean(np.square(X_scaled - reconstructed))

    # -------------------------
    # Step 3: check anomaly
    # -------------------------
    if error < THRESHOLD:
        return {"status": "NORMAL", "stage": "autoencoder", "error": float(error)}

    # -------------------------
    # Step 4: CNN-BiLSTM classification
    # -------------------------
    X_reshaped = X_scaled.reshape(1, X_scaled.shape[1], 1)

    prediction = classifier.predict(X_reshaped)

    class_id = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "status": "ANOMALY",
        "stage": "cnn_bilstm",
        "attack_class": class_id,
        "confidence": confidence,
        "error": float(error),
    }


# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("serve:app", host="0.0.0.0", port=8000, reload=True)
