# scripts/coleta/coleta_cripto.py
import requests
import pandas as pd
from datetime import datetime

def coletar_dados():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '30',
        'interval': 'daily'
    }
    r = requests.get(url, params=params)
    data = r.json()
    prices = pd.DataFrame(data['prices'], columns=["timestamp", "price"])
    prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')
    prices.to_csv('dados/btc.csv', index=False)
    print("Dados salvos em dados/btc.csv")

if __name__ == "__main__":
    coletar_dados()

