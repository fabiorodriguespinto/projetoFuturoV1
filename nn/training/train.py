##nn/training/train.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def treinar_modelo():
    print("Treinando modelo...")

    # Leitura de dados simulada
    df = pd.read_csv("/data/input/bitcoin_daily_30d.csv")

    # Criação de features simples (só para fins de exemplo)
    df["dia"] = df.index
    X = df[["dia"]]
    y = df["price"]

    # Treinamento
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Salvando modelo
    os.makedirs("/data/modelo", exist_ok=True)
    joblib.dump(modelo, "/data/modelo/modelo.pkl")
    print("Modelo salvo em /data/modelo/modelo.pkl")
