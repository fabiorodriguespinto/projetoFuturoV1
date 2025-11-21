##neural_network/training/train.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
from datetime import datetime
from shared import config

def treinar_modelo():
    print("🤖 Iniciando treinamento do modelo...")

    # Carrega os dados
    df = pd.read_csv(config.CAMINHO_DADOS)

    # Gera as novas features
    df["dia"] = pd.to_datetime(df["open_time"]).dt.dayofyear
    df["media"] = (df["high"] + df["low"]) / 2
    df["var_percent"] = ((df["high"] - df["low"]) / df["open"]) * 100

    # Define as features e variável alvo
    X = df[["open", "high", "low", "volume", "dia", "media", "var_percent"]]
    y = df["close"]

    # Treinamento
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Gera nome com timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"modelo_{timestamp}.pkl"
    caminho_modelo = os.path.join(config.DIRETORIO_MODELO, nome_arquivo)

    # Salva o modelo
    os.makedirs(config.DIRETORIO_MODELO, exist_ok=True)
    joblib.dump(modelo, caminho_modelo)
    print(f"✅ Modelo salvo em: {caminho_modelo}")

    # Cria/atualiza o link simbólico
    link_simbolico = os.path.join(config.DIRETORIO_MODELO, "modelo_mais_recente.pkl")
    if os.path.islink(link_simbolico) or os.path.exists(link_simbolico):
        os.remove(link_simbolico)
    os.symlink(nome_arquivo, link_simbolico)
    print(f"🔗 Link simbólico criado: {link_simbolico} -> {nome_arquivo}")

