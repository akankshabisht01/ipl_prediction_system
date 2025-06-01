import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import os
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ipl_prediction_model.pkl')

def load_model():
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
            logger.info("Model loaded successfully")
            return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
try:
    model = load_model()
    logger.info("Model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize model: {e}")
    raise

class PredictionInput(BaseModel):
    batting_team: str
    bowling_team: str
    venue: str
    runs_left: float
    balls_left: float
    wickets_left: float
    total_runs_x: float
    crr: float
    rrr: float

@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        logger.info(f"Received prediction request: {input_data}")

        # Compute additional features
        run_rate_ratio = input_data.crr / input_data.rrr if input_data.rrr != 0 else 0
        pressure_index = (input_data.runs_left * input_data.rrr) / (input_data.wickets_left + 1)
        death_over_impact = 1.5 if input_data.balls_left <= 24 else 1.0
        wicket_impact = (10 - input_data.wickets_left) * death_over_impact
        runs_per_ball = input_data.runs_left / input_data.balls_left if input_data.balls_left != 0 else 0
        required_boundaries = input_data.runs_left / 4
        overs_remaining = input_data.balls_left / 6
        run_rate_diff = input_data.crr - input_data.rrr

        # Prepare input DataFrame with all 16 features
        input_df = pd.DataFrame([{
            'batting_team': input_data.batting_team,
            'bowling_team': input_data.bowling_team,
            'venue': input_data.venue,
            'runs_left': input_data.runs_left,
            'balls_left': input_data.balls_left,
            'wickets_left': input_data.wickets_left,
            'total_runs_x': input_data.total_runs_x,
            'crr': input_data.crr,
            'rrr': input_data.rrr,
            'run_rate_ratio': run_rate_ratio,
            'pressure_index': pressure_index,
            'wicket_impact': wicket_impact,
            'runs_per_ball': runs_per_ball,
            'required_boundaries': required_boundaries,
            'overs_remaining': overs_remaining,
            'run_rate_diff': run_rate_diff
        }])

        logger.info(f"Features DataFrame for prediction: {input_df}")

        # Predict
        prediction = model.predict_proba(input_df)[0]
        logger.info(f"Raw prediction: {prediction}")
        batting_win = float(prediction[1])
        bowling_win = float(prediction[0])

        # Validate probabilities
        if not (0 <= batting_win <= 1 and 0 <= bowling_win <= 1):
            logger.error(f"Invalid probability values: batting={batting_win}, bowling={bowling_win}")
            raise HTTPException(status_code=500, detail="Invalid probability values")

        logger.info(f"Final probabilities - batting: {batting_win}, bowling: {bowling_win}")

        return {
            "batting_win": batting_win,
            "bowling_win": bowling_win
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "IPL Prediction API is running"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
