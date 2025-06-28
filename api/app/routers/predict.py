##api/app/routers/predict.py

from fastapi import APIRouter
from nn.inference.predict import prever  # novo import

router = APIRouter()

@router.post("/predict")
def predict():
    try:
        valor = prever()
        return {"prediction": valor}
    except Exception as e:
        return {"error": str(e)}
