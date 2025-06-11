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

# Sample data for fitting the preprocessor
SAMPLE_DATA = {
    'batting_team': ['Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore', 
                    'Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings', 
                    'Rajasthan Royals', 'Sunrisers Hyderabad', 'Gujarat Titans', 
                    'Lucknow Super Giants'],
    'bowling_team': ['Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders',
                    'Royal Challengers Bangalore', 'Delhi Capitals', 'Punjab Kings',
                    'Rajasthan Royals', 'Sunrisers Hyderabad', 'Gujarat Titans',
                    'Lucknow Super Giants'],
    'city': ['Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Delhi', 'Punjab',
            'Jaipur', 'Hyderabad', 'Gujarat', 'Lucknow'],
    'runs_left': [50, 75, 100],
    'balls_left': [30, 45, 60],
    'wickets': [5, 6, 7],
    'total_runs_x': [150, 180, 200],
    'crr': [8.5, 9.0, 7.5],
    'rrr': [10.0, 12.0, 8.0]
}

class MatchInput(BaseModel):
    batting_team: str
    bowling_team: str
    venue: str
    runs_left: int
    balls_left: int
    wickets_left: int
    target_runs: int  # Changed from total_runs_x
    crr: float
    rrr: float

def create_and_fit_preprocessor():
    """Create and fit the preprocessor with sample data"""
    # Define numerical and categorical features
    numerical_features = ['runs_left', 'balls_left', 'wickets', 'total_runs_x', 'crr', 'rrr']
    categorical_features = ['batting_team', 'bowling_team', 'city']
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ])
    
    # Fit preprocessor with sample data
    sample_df = pd.DataFrame(SAMPLE_DATA)
    preprocessor.fit(sample_df)
    
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
        preprocessor = create_and_fit_preprocessor()
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
        
        # Convert venue to city
        venue_to_city = {
            'Wankhede Stadium, Mumbai': 'Mumbai',
            'M. A. Chidambaram Stadium, Chennai': 'Chennai',
            'Eden Gardens, Kolkata': 'Kolkata',
            'Arun Jaitley Stadium, Delhi': 'Delhi',
            'M. Chinnaswamy Stadium, Bengaluru': 'Bengaluru',
            'Punjab Cricket Association IS Bindra Stadium, Mohali': 'Punjab',
            'Sawai Mansingh Stadium, Jaipur': 'Jaipur',
            'Rajiv Gandhi International Cricket Stadium, Hyderabad': 'Hyderabad',
            'Sardar Patel Stadium (Narendra Modi Stadium), Ahmedabad': 'Gujarat',
            'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow': 'Lucknow'
        }
        
        # Create input data
        input_data = {
            'batting_team': match.batting_team,
            'bowling_team': match.bowling_team,
            'city': venue_to_city.get(match.venue, 'Mumbai'),  # Default to Mumbai if venue not found
            'runs_left': match.runs_left,
            'balls_left': match.balls_left,
            'wickets': match.wickets_left,
            'total_runs_x': match.target_runs,  # Map target_runs to total_runs_x
            'crr': match.crr,
            'rrr': match.rrr
        }
        
        # Create DataFrame for preprocessing
        input_df = pd.DataFrame([input_data])
        
        # Log the input data for debugging
        logger.info(f"Input data: {input_data}")
        
        # Transform features
        transformed_features = preprocessor.transform(input_df)
        
        # Log the shape of transformed features
        logger.info(f"Transformed features shape: {transformed_features.shape}")
        
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