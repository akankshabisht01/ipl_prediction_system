import os
import pickle
import logging
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="IPL Match Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ipl-prediction-system-two.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Storage settings
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "model")
MODEL_BLOB_NAME = os.getenv("MODEL_BLOB_NAME", "ipl_prediction_model.pkl")
MODEL_PATH = "model.pkl"

# Initialize model variable
model = None

class MatchInput(BaseModel):
    batting_team: str
    bowling_team: str
    city: str
    current_score: int
    balls_left: int
    wickets_left: int
    last_five: List[int]

def download_model():
    """Download the model file if it doesn't exist"""
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model file from Azure Blob Storage...")
        try:
            # Create the BlobServiceClient
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
            
            # Get the container client
            container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
            
            # Get the blob client
            blob_client = container_client.get_blob_client(MODEL_BLOB_NAME)
            
            # Download the blob
            logger.info(f"Downloading model from blob: {MODEL_BLOB_NAME}")
            with open(MODEL_PATH, "wb") as download_file:
                download_data = blob_client.download_blob()
                download_file.write(download_data.readall())
            
            # Verify the downloaded file
            try:
                with open(MODEL_PATH, 'rb') as f:
                    test_load = pickle.load(f)
                logger.info("Model downloaded and verified successfully")
            except Exception as e:
                logger.error(f"Downloaded file is not a valid pickle file: {str(e)}")
                if os.path.exists(MODEL_PATH):
                    os.remove(MODEL_PATH)
                raise Exception("Downloaded file is not a valid pickle file")
                
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            raise Exception(f"Model download failed: {str(e)}. Please ensure the Azure Blob Storage connection is correct.")

def load_model():
    """Load the model from file"""
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            download_model()
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise Exception(f"Model loading failed: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Load the model when the application starts"""
    try:
        load_model()
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "IPL Match Prediction API is running"}

@app.post("/predict")
async def predict_score(match: MatchInput):
    try:
        if model is None:
            load_model()
        
        # Create input array for prediction
        input_data = np.array([[
            match.current_score,
            match.balls_left,
            match.wickets_left,
            *match.last_five,
            # Add team and city encoding here if needed
        ]])
        
        # Make prediction
        prediction = model.predict(input_data)
        
        return {
            "predicted_score": int(prediction[0]),
            "input_data": match.dict()
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 