# nn/inference/predict.py

import pandas as pd
import joblib
import os

def prever():
    caminho_modelo = "/data/modelo/modelo.pkl"
    caminho_dados = "/data/input/bitcoin_daily_30d.csv"

    if not os.path.exists(caminho_modelo):
        raise FileNotFoundError("Modelo não encontrado!")

    if not os.path.exists(caminho_dados):
        raise FileNotFoundError("Dados de entrada não encontrados!")

    modelo = joblib.load(caminho_modelo)
    df = pd.read_csv(caminho_dados)

    # ✅ Prepara os dados com a mesma coluna usada no treino
    X_novo = pd.DataFrame([[len(df)]], columns=["dia"])

    predicao = modelo.predict(X_novo)

    return float(predicao[0])
