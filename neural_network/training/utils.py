##nn/training/utils.py

import pandas as pd
from shared import config

def preparar_dados():
    df = pd.read_csv(config.CAMINHO_DADOS)

    df["dia"] = pd.to_datetime(df["open_time"]).dt.dayofyear
    df["media"] = (df["high"] + df["low"]) / 2
    df["var_percent"] = ((df["high"] - df["low"]) / df["open"]) * 100
    df["target"] = df["close"].shift(-config.ANTECEDENCIA_CANDLES)
    df.dropna(inplace=True)

    X = df[["open", "high", "low", "volume", "dia", "media", "var_percent"]]
    y = df["target"]
    return X, y


