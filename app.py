from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Load prepared data and best model
data = pd.read_csv("prepared_data.csv", parse_dates=["timestamp"]).set_index("timestamp")["temp"]
from statsmodels.tsa.arima.model import ARIMAResults
model = ARIMAResults.load("best_model.pkl")

class PredictRequest(BaseModel):
    steps: int

@app.post("/predict")
def predict(req: PredictRequest):
    forecast = model.forecast(steps=req.steps)
    return {"forecast": forecast.tolist()}
