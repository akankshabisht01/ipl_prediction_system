import os
import pickle
import logging
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from pydantic import BaseModel
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="IPL Match Prediction API")

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

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "model")
MODEL_BLOB_NAME = os.getenv("MODEL_BLOB_NAME", "ipl_prediction_model.pkl")
MODEL_PATH = "model.pkl"

model = None

def download_model():
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model file from Azure Blob Storage...")
        try:
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
            blob_client = container_client.get_blob_client(MODEL_BLOB_NAME)
            with open(MODEL_PATH, "wb") as download_file:
                download_data = blob_client.download_blob()
                download_file.write(download_data.readall())
            with open(MODEL_PATH, 'rb') as f:
                test_load = pickle.load(f)
            logger.info("Model downloaded and verified successfully")
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            raise Exception(f"Model download failed: {str(e)}. Please ensure the Azure Blob Storage connection is correct.")

def load_model():
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

@app.exception_handler(FastAPIRequestValidationError)
async def validation_exception_handler(request: Request, exc: FastAPIRequestValidationError):
    logger.error(f"422 Validation Error: {exc.errors()} | Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": (await request.body()).decode('utf-8')}
    )

@app.on_event("startup")
async def startup_event():
    try:
        load_model()
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "IPL Match Prediction API is running"}

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

@app.post("/predict")
async def predict_score(match: MatchInput):
    try:
        if model is None:
            load_model()
        # Compute advanced features
        run_rate_ratio = match.crr / match.rrr if match.rrr != 0 else 0
        pressure_index = (match.runs_left * match.rrr) / (match.wickets_left + 1)
        death_over_impact = 1.5 if match.balls_left <= 24 else 1.0
        wicket_impact = (10 - match.wickets_left) * death_over_impact
        runs_per_ball = match.runs_left / match.balls_left if match.balls_left != 0 else 0
        required_boundaries = match.runs_left / 4
        overs_remaining = match.balls_left / 6
        run_rate_diff = match.crr - match.rrr
        # Build DataFrame in correct order
        input_data = pd.DataFrame({
            'batting_team': [match.batting_team],
            'bowling_team': [match.bowling_team],
            'venue': [match.venue],
            'runs_left': [match.runs_left],
            'balls_left': [match.balls_left],
            'wickets_left': [match.wickets_left],
            'total_runs_x': [match.total_runs_x],
            'crr': [match.crr],
            'rrr': [match.rrr],
            'run_rate_ratio': [run_rate_ratio],
            'pressure_index': [pressure_index],
            'wicket_impact': [wicket_impact],
            'runs_per_ball': [runs_per_ball],
            'required_boundaries': [required_boundaries],
            'overs_remaining': [overs_remaining],
            'run_rate_diff': [run_rate_diff]
        })
        proba = model.predict_proba(input_data)
        win_prob = proba[0, 1]
        lose_prob = proba[0, 0]
        return {
            "batting_team_win_probability": round(win_prob * 100, 2),
            "bowling_team_win_probability": round(lose_prob * 100, 2)
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 