##neural_network/training/train_linear.py

import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from shared.market_data import carregar_candles
import os

MODELOS_DIR = "/data/modelos"
os.makedirs(MODELOS_DIR, exist_ok=True)

def treinar_linear():
    df = carregar_candles(limit=5000)

    df["return"] = df["close"].pct_change()
    df.dropna(inplace=True)

    X = df[["open", "high", "low", "close", "volume", "return"]]
    y = df["close"].shift(-1).dropna()
    X = X.iloc[:-1]

    modelo = LinearRegression()
    modelo.fit(X, y)

    caminho = os.path.join(MODELOS_DIR, "linear_regression.pkl")
    joblib.dump(modelo, caminho)

    print(f"Modelo salvo em: {caminho}")


if __name__ == "__main__":
    treinar_linear()
