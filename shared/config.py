## shared/config.py

import os

# ---------------------------------------------
# Parâmetros gerais
# ---------------------------------------------
ATIVO = os.getenv("ATIVO", "BTCUSDT")
INTERVALO = os.getenv("INTERVALO", "1m")

# Quantidade de candles utilizados pela IA
NUM_CANDLES_USADOS = int(os.getenv("NUM_CANDLES_USADOS", 60))

# Quantidade de candles para coleta
QUANTIDADE_CANDLES = int(os.getenv("QUANTIDADE_CANDLES", 300))


# ---------------------------------------------
# Caminhos e modelos
# ---------------------------------------------
CAMINHO_DADOS = f"/data/input/{ATIVO}_{INTERVALO}.csv"
DIRETORIO_MODELO = "/data/modelo"

NOME_MODELO = os.getenv("NOME_MODELO", "LinearRegression")
CAMINHO_MODELO = f"{DIRETORIO_MODELO}/modelo_{NOME_MODELO}.pkl"

