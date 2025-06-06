import fastapi
import joblib
import pandas as pd
import uvicorn
from pydantic import BaseModel

# Define the input data model
class PredictionRequest(BaseModel):
    day_of_year: int

# Initialize FastAPI app
app = fastapi.FastAPI()

# Load the model (consider loading this at startup if it's large)
# Path is relative to main.py inside the container WORKDIR /app/nn
# Models are mounted to /app/nn/modelos
MODEL_PATH = "modelos/modelo_btc.pkl"

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        # Load model
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        raise fastapi.HTTPException(status_code=500, detail="Model file not found.")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

    try:
        # Prepare data for prediction
        # The model expects a DataFrame with a 'dia' column (consistent with training)
        data = pd.DataFrame([[request.day_of_year]], columns=['dia'])

        # Make prediction
        prediction = model.predict(data)

        # Return prediction
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

if __name__ == "__main__":
    # This is for local development/testing only
    # The Docker CMD will run uvicorn directly
    uvicorn.run(app, host="0.0.0.0", port=8001)
