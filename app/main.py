from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# Initialize the API
app = FastAPI(title="Waste Paper Revenue API")

# Load the trained model into memory when the app starts
MODEL_PATH = "models/model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# Define the exact data structure the API expects (Data Validation)
class PredictionRequest(BaseModel):
    Month: int
    Quarter: int
    Revenue_lag_1: float
    Rolling_avg_3: float

# Create the prediction endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    # Failsafe if the model file is missing
    if model is None:
        raise HTTPException(status_code=500, detail="Model file not found. Train the model first.")
    
    # Convert the incoming JSON payload into a pandas DataFrame
    df = pd.DataFrame([request.model_dump()])
    
    # Run the prediction
    prediction = model.predict(df[['Month', 'Quarter', 'Revenue_lag_1', 'Rolling_avg_3']])
    
    # Return the result as JSON
    return {"predicted_revenue": round(float(prediction[0]), 2)}