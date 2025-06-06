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
import gdown

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
            file_id = None
            patterns = [
                r'/d/(.*?)/view',  # Standard sharing URL
                r'id=([^&]+)',     # Direct ID format
                r'/file/d/(.*?)/'  # Alternative sharing URL
            ]
            
            for pattern in patterns:
                match = re.search(pattern, model_url)
                if match:
                    file_id = match.group(1)
                    break
            
            if not file_id:
                raise Exception("Could not extract file ID from URL")
            
            logger.info(f"Extracted file ID: {file_id}")
            
            # Use gdown to download the file with the correct URL format
            output = MODEL_PATH
            url = f'https://drive.google.com/uc?id={file_id}'
            
            # Add retry logic with exponential backoff
            max_retries = 5
            base_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"Download attempt {attempt + 1} of {max_retries}")
                    
                    # First try with gdown's direct download
                    try:
                        gdown.download(url=url, output=output, quiet=False, fuzzy=True)
                    except Exception as e:
                        logger.warning(f"gdown fuzzy download failed: {str(e)}")
                        # If fuzzy fails, try direct download
                        gdown.download(url=url, output=output, quiet=False, fuzzy=False)
                    
                    # If gdown fails, try requests with proper headers
                    if not os.path.exists(MODEL_PATH):
                        logger.info("Trying alternative download method...")
                        session = requests.Session()
                        
                        # Set up headers to mimic a browser
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                        
                        # First get the confirmation page
                        response = session.get(url, headers=headers, stream=True)
                        response.raise_for_status()
                        
                        # Check if we got an HTML page (confirmation page)
                        if '<html' in response.text.lower():
                            logger.info("Received confirmation page, proceeding with download...")
                            # Extract the download URL from the confirmation page
                            download_url = response.url
                            if 'confirm=' in download_url:
                                # Add the confirm parameter
                                download_url += '&confirm=t'
                            
                            # Download the actual file
                            response = session.get(download_url, headers=headers, stream=True)
                            response.raise_for_status()
                        
                        # Save the file
                        with open(output, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                    
                    if os.path.exists(MODEL_PATH):
                        try:
                            with open(MODEL_PATH, 'rb') as f:
                                test_load = pickle.load(f)
                            logger.info("Model downloaded and verified successfully")
                            return
                        except Exception as e:
                            logger.error(f"Downloaded file is not a valid pickle file: {str(e)}")
                            if os.path.exists(MODEL_PATH):
                                os.remove(MODEL_PATH)
                            raise Exception("Downloaded file is not a valid pickle file")
                    else:
                        raise Exception("File download failed")
                        
                except Exception as e:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Download attempt {attempt + 1} failed: {str(e)}")
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        raise Exception(f"Failed to download model after {max_retries} attempts: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            raise Exception(f"Model download failed: {str(e)}. Please ensure the file is publicly accessible on Google Drive and the sharing link is correct.")

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
