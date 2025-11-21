##neural_network/training/train.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def treinar_modelo():
    print("📚 Iniciando treinamento do modelo...")

    # Caminho para o arquivo CSV
    csv_path = "/data/input/bitcoin_daily_30d.csv"
    df = pd.read_csv(csv_path)

    # Garante que os dados necessários estão presentes
    features = ["open", "high", "low", "volume"]
    target = "close"  # Previsão do preço de fechamento

    for coluna in features + [target]:
        if coluna not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {coluna}")

    # Remove possíveis NaNs
    df.dropna(subset=features + [target], inplace=True)

    # Separa X e y
    X = df[features]
    y = df[target]

    # Treina o modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Salva o modelo
    os.makedirs("/data/modelo", exist_ok=True)
    joblib.dump(modelo, "/data/modelo/modelo.pkl")
    print("✅ Modelo treinado e salvo em /data/modelo/modelo.pkl")
