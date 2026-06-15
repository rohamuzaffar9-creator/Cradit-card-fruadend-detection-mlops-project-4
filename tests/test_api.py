from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.main import app

client = TestClient(app)

SAMPLE = [0.0,-1.36,-0.07,2.54,1.38,-0.34,0.46,0.24,
          0.10,0.36,0.09,-0.55,-0.62,-0.99,-0.31,1.47,
          -0.47,0.21,0.02,0.40,0.25,-0.02,0.28,-0.11,
          0.07,0.13,-0.19,0.13,-0.02,149.62]

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["sap_id"] == "70149156"

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_predict_returns_label():
    r = client.post("/predict", json={"features": SAMPLE})
    assert r.status_code == 200
    body = r.json()
    assert "label" in body
    assert body["label"] in ["FRAUD", "LEGITIMATE"]
    assert 0.0 <= body["fraud_probability"] <= 1.0

def test_predict_wrong_feature_count():
    r = client.post("/predict", json={"features": [1.0, 2.0]})
    assert r.status_code == 422
