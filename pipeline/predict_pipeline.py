import numpy as np
import joblib
from tensorflow.keras.models import load_model

# -----------------------
# Load models
# -----------------------
autoencoder = load_model("models/autoencoder.h5")
classifier = load_model("models/cnn_bilstm.h5")
scaler = joblib.load("models/scaler.pkl")

# -----------------------
# Threshold (you should store this from training ideally)
# -----------------------
THRESHOLD = 0.05  # or load from file later


# -----------------------
# Main pipeline function
# -----------------------
def predict_traffic(features):

    # Step 1: preprocess
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)

    # Step 2: AUTOENCODER (anomaly detection)
    reconstructed = autoencoder.predict(features_scaled)

    error = np.mean(np.square(features_scaled - reconstructed))

    # Step 3: check anomaly
    if error < THRESHOLD:
        return {"status": "NORMAL", "error": float(error)}

    # Step 4: CNN-BiLSTM classification
    features_reshaped = features_scaled.reshape(1, features_scaled.shape[1], 1)

    prediction = classifier.predict(features_reshaped)
    class_id = int(np.argmax(prediction))

    return {"status": "ANOMALY", "attack_class": class_id, "error": float(error)}
