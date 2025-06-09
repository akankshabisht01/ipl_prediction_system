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
import time
import gdown
import requests
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient

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

# Model path - using absolute path
MODEL_PATH = os.path.join(os.getcwd(), "model.pkl")

# Azure Storage configuration
STORAGE_ACCOUNT_NAME = "model01"
CONTAINER_NAME = "model"
SAS_TOKEN = "?sp=r&st=2025-06-09T21:24:49Z&se=2027-01-01T05:24:49Z&spr=https&sv=2024-11-04&sr=c&sig=AvJqgx%2FOjwlS0unxKWyiAiI37%2FESVxWXrDwsHeENHsc%3D"

def download_model():
    """Download the model file if it doesn't exist"""
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model file from Azure Blob Storage...")
        try:
            # Create the BlobServiceClient
            blob_service_client = BlobServiceClient(
                account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
                credential=SAS_TOKEN
            )
            
            # Get the container client
            container_client = blob_service_client.get_container_client(CONTAINER_NAME)
            
            # List blobs in the container
            blob_list = container_client.list_blobs()
            model_blob = None
            
            # Find the .pkl file
            for blob in blob_list:
                if blob.name.endswith('.pkl'):
                    model_blob = blob
                    break
            
            if not model_blob:
                raise Exception("No .pkl file found in the container")
            
            logger.info(f"Found model file: {model_blob.name}")
            
            # Get the blob client
            blob_client = container_client.get_blob_client(model_blob.name)
            
            # Download the blob
            logger.info("Starting download...")
            with open(MODEL_PATH, "wb") as download_file:
                download_data = blob_client.download_blob()
                download_file.write(download_data.readall())
            
            logger.info("Model downloaded successfully")
            
            # Verify the downloaded file
            try:
                with open(MODEL_PATH, 'rb') as f:
                    test_load = pickle.load(f)
                logger.info("Model verified successfully")
            except Exception as e:
                logger.error(f"Downloaded file is not a valid pickle file: {str(e)}")
                if os.path.exists(MODEL_PATH):
                    os.remove(MODEL_PATH)
                raise Exception("Downloaded file is not a valid pickle file")
                
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            raise Exception(f"Model download failed: {str(e)}. Please ensure the Azure Blob Storage configuration is correct.")

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

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
