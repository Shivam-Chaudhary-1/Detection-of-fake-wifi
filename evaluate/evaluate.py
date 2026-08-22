from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report
import numpy as np

model = load_model("models/cnn_bilstm.h5")

y_pred = model.predict(X_test)

print(classification_report(y_test, np.argmax(y_pred, axis=1)))
