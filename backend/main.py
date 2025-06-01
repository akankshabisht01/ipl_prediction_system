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
import requests
import re
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model path
MODEL_PATH = "ipl_prediction_model.pkl"

def download_model():
    """Download the model file if it doesn't exist"""
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model file...")
        model_url = os.getenv("MODEL_URL")
        if not model_url:
            raise Exception("MODEL_URL environment variable not set")
        
        try:
            # Extract file ID from Google Drive URL
            file_id = re.search(r'/d/(.*?)/view', model_url)
            if not file_id:
                raise Exception("Invalid Google Drive URL")
            file_id = file_id.group(1)
            
            # Create a session to handle cookies
            session = requests.Session()
            
            # First request to get the confirmation token
            url = f"https://drive.google.com/uc?id={file_id}&export=download"
            response = session.get(url, stream=True)
            
            # Check if we need to handle the confirmation page
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
                    response = session.get(url, stream=True)
                    break
            
            # Download the file
            if response.status_code == 200:
                # Save the response content to a temporary file first
                temp_path = f"{MODEL_PATH}.temp"
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify the file is a valid pickle file
                try:
                    with open(temp_path, 'rb') as f:
                        # Try to load the pickle file
                        test_load = pickle.load(f)
                    # If successful, rename the temp file to the actual model file
                    os.rename(temp_path, MODEL_PATH)
                    logger.info("Model downloaded and verified successfully")
                except Exception as e:
                    logger.error(f"Downloaded file is not a valid pickle file: {str(e)}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    raise Exception("Downloaded file is not a valid pickle file")
            else:
                raise Exception(f"Failed to download model: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            raise

def load_model():
    """Load the ML model"""
    try:
        download_model()
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
            logger.info("Model loaded successfully")
            return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load ML model")

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
