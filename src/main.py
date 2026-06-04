from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import joblib
import numpy as np
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Real-Time Fraud Detection API",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)

MODEL_PATH = os.getenv("MODEL_PATH", "models/fraud_model.pkl")
model = None

@app.on_event("startup")
async def load_model():
    global model
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")

class Transaction(BaseModel):
    features: List[float] = Field(..., min_length=30, max_length=30)

@app.get("/")
def root():
    return {"project": "Real-Time Fraud Detection System", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict(transaction: Transaction):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    X = np.array(transaction.features).reshape(1, -1)
    prediction = int(model.predict(X)[0])
    probability = float(model.predict_proba(X)[0][1])
    return {
        "prediction": prediction,
        "label": "FRAUD" if prediction == 1 else "LEGITIMATE",
        "fraud_probability": round(probability, 4),
    }
