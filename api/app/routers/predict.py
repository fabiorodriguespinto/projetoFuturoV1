from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import yaml
import os
from datetime import datetime # Although not strictly used in the final code, good to have for date ops

router = APIRouter()

# Configuration Loading
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../../config/config.yaml')
DEFAULT_NN_SERVICE_URL = "http://nn_service:8001/predict_fallback" # Fallback if config fails

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as stream:
            config = yaml.safe_load(stream)
        url = config.get('nn_service_url')
        if not url:
            print(f"ERROR: 'nn_service_url' not found in {CONFIG_PATH}. Using default.", flush=True)
            return DEFAULT_NN_SERVICE_URL
        print(f"Loaded NN_SERVICE_URL: {url} from {CONFIG_PATH}", flush=True)
        return url
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {CONFIG_PATH}. Using default.", flush=True)
        return DEFAULT_NN_SERVICE_URL
    except yaml.YAMLError as exc:
        print(f"ERROR: Error parsing YAML configuration file {CONFIG_PATH}: {exc}. Using default.", flush=True)
        return DEFAULT_NN_SERVICE_URL
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while loading config: {e}. Using default.", flush=True)
        return DEFAULT_NN_SERVICE_URL

NN_SERVICE_URL = load_config()

class PredictionInput(BaseModel):
    day_of_year: int

@router.post("/predictions", summary="Create a new prediction by calling the NN service")
async def create_prediction(prediction_input: PredictionInput):
    """
    Receives a day_of_year, calls the NN inference service, and returns its prediction.
    """
    payload = {"day_of_year": prediction_input.day_of_year}

    try:
        response = requests.post(NN_SERVICE_URL, json=payload, timeout=10) # 10 second timeout
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)

        # Assuming NN service returns {"prediction": <float>}
        prediction_data = response.json()

        if "prediction" not in prediction_data:
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from NN service: 'prediction' key missing."
            )

        return prediction_data # Return the full JSON from NN service

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504, # Gateway Timeout
            detail=f"Request to NN service timed out."
        )
    except requests.exceptions.RequestException as e:
        # This catches connection errors, non-200 status codes (due to raise_for_status), etc.
        error_detail = f"Error calling NN service: {str(e)}"
        # If the error is an HTTPError from a 4xx/5xx response from the NN service itself
        if e.response is not None:
             error_detail = f"NN service returned status {e.response.status_code}: {e.response.text}"
             # For specific NN service errors, we might want to use a 502 Bad Gateway
             raise HTTPException(status_code=502, detail=error_detail)

        raise HTTPException(
            status_code=503, # Service Unavailable for connection issues or other generic errors
            detail=error_detail
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500, # Internal Server Error
            detail=f"An unexpected error occurred: {str(e)}"
        )
