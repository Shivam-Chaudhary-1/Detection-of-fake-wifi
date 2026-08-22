import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../dataset/awid.csv")

X = df.drop("label", axis=1)
y = df["label"]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "../models/scaler.pkl")
