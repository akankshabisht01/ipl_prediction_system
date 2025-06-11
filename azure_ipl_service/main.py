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
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="IPL Match Prediction API")

# Add CORS middleware with more specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ipl-prediction-system-two.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Azure Storage settings
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "model")
MODEL_BLOB_NAME = os.getenv("MODEL_BLOB_NAME", "ipl_prediction_model.pkl")
MODEL_PATH = "model.pkl"

# Initialize model and preprocessor variables
model = None
preprocessor = None

class MatchInput(BaseModel):
    batting_team: str
    bowling_team: str
    venue: str
    runs_left: int
    balls_left: int
    wickets_left: int
    total_runs_x: int
    crr: float
    rrr: float

def create_preprocessor():
    """Create the preprocessor for feature transformation"""
    # Define numerical and categorical features
    numerical_features = ['runs_left', 'balls_left', 'wickets_left', 'total_runs_x', 'crr', 'rrr']
    categorical_features = ['batting_team', 'bowling_team', 'venue']
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    return preprocessor

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
    global model, preprocessor
    try:
        if not os.path.exists(MODEL_PATH):
            download_model()
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        preprocessor = create_preprocessor()
        logger.info("Model and preprocessor loaded successfully")
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
        if model is None or preprocessor is None:
            load_model()
        
        # Create DataFrame for preprocessing
        input_df = pd.DataFrame([match.dict()])
        
        # Transform features
        transformed_features = preprocessor.transform(input_df)
        
        # Make prediction
        prediction = model.predict(transformed_features)
        
        # Calculate win probabilities
        batting_win = float(prediction[0])
        bowling_win = 1 - batting_win
        
        return {
            "batting_win": batting_win,
            "bowling_win": bowling_win,
            "input_data": match.dict()
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 