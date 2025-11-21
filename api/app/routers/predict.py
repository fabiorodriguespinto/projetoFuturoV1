from fastapi import APIRouter
from shared.database import carregar_candles
from shared import config
import joblib
import numpy as np
import pandas as pd
import os

router = APIRouter(prefix="/predict", tags=["Predição"])

MODEL_DIR = "/app/neural_network/models/"


@router.post("/")
def prever():
    df = carregar_candles(limit=config.NUM_CANDLES_USADOS)

    if df is None or len(df) < config.NUM_CANDLES_USADOS:
        return {"erro": "Dados insuficientes no banco."}

    X = df.tail(config.NUM_CANDLES_USADOS)["close"].pct_change().fillna(0).values
    X = np.array([X])

    modelos = {}
    previsoes = []

    for nome_arquivo in os.listdir(MODEL_DIR):
        if nome_arquivo.endswith(".pkl"):
            modelo = joblib.load(os.path.join(MODEL_DIR, nome_arquivo))
            y = modelo.predict(X)[0]
            modelos[nome_arquivo] = float(y)
            previsoes.append(y)

    if not previsoes:
        return {"erro": "Nenhum modelo encontrado."}

    previsao_final = float(np.mean(previsoes))

    return {
        "prediction": previsao_final,
        "models": modelos
    }
