# nn/inference/predict.py

import numpy as np
import joblib
import os
import glob
import pandas as pd
from shared.market_data import carregar_candles

# Caminho padrão para modelos
MODELOS_DIR = "/data/modelos"


# ----------------------------------------------------
# CARREGAR MODELOS
# ----------------------------------------------------
def carregar_modelos():
    modelos = {}
    arquivos = glob.glob(os.path.join(MODELOS_DIR, "*.pkl"))

    for caminho in arquivos:
        nome = os.path.basename(caminho).replace(".pkl", "")
        modelos[nome] = joblib.load(caminho)

    return modelos


# ----------------------------------------------------
# PREVER PREÇO
# ----------------------------------------------------
def prever():
    # LER DADOS DO POSTGRES
    df = carregar_candles(limit=200)

    # CRIA FEATURES SIMPLES (você pode expandir isso depois)
    df["return"] = df["close"].pct_change()
    df.dropna(inplace=True)

    X = df[["open", "high", "low", "close", "volume", "return"]].values[-1].reshape(1, -1)

    modelos = carregar_modelos()
    previsoes = {}

    for nome, modelo in modelos.items():
        previsoes[nome] = float(modelo.predict(X)[0])

    media_previsoes = np.mean(list(previsoes.values()))

    return float(media_previsoes), previsoes
