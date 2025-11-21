# shared/market_data.py

import requests
import pandas as pd
from sqlalchemy import text
from shared.database import engine, SessionLocal
from shared.models import Candle
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# SALVAR CANDLES NO POSTGRES
# ---------------------------------------------------------
def salvar_candles(df: pd.DataFrame):
    try:
        df.to_sql("candles", engine, if_exists="append", index=False)
        logger.info(f"{len(df)} candles inseridos no banco.")
    except Exception as e:
        logger.error(f"Erro ao salvar candles: {e}")


# ---------------------------------------------------------
# CARREGAR CANDLES DO POSTGRES
# ---------------------------------------------------------
def carregar_candles(limit=500):
    query = text("""
        SELECT open_time, open, high, low, close, volume
        FROM candles
        ORDER BY open_time DESC
        LIMIT :limit
    """)

    df = pd.read_sql(query, engine, params={"limit": limit})
    df.sort_values("open_time", inplace=True)
    return df


# ---------------------------------------------------------
# COLETAR CANDLES DA BINANCE E SALVAR NO BANCO
# ---------------------------------------------------------
def coletar_candles_binance(symbol="BTCUSDT", interval="1m", limit=500):
    url = (
        "https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}&interval={interval}&limit={limit}"
    )

    try:
        data = requests.get(url, timeout=10).json()
    except Exception as e:
        logger.error(f"Erro ao coletar dados da Binance: {e}")
        return None

    candles = []
    for k in data:
        candles.append(
            {
                "open_time": datetime.fromtimestamp(k[0] / 1000),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
            }
        )

    df = pd.DataFrame(candles)

    # salvar no banco
    salvar_candles(df)

    return df
