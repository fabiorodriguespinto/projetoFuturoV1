#worker/market_colletctor.py

import requests
import pandas as pd
from shared.database import engine

def coletar_candles(symbol="BTCUSDT", interval="1m", limit=500):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()

    rows = []
    for k in data:
        rows.append({
            "open_time": pd.to_datetime(k[0], unit="ms"),
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
        })

    df = pd.DataFrame(rows)
    df.to_sql("candles", engine, if_exists="append", index=False)
