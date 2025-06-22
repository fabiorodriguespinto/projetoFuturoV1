## worker/tasks/coleta_cripto.py
import requests
import pandas as pd
from datetime import datetime
import os
import argparse

def coletar_dados(ativo='bitcoin', vs_currency='usd', dias=30, intervalo='daily', output_path='data/input'):
    url = f'https://api.coingecko.com/api/v3/coins/{ativo}/market_chart'
    params = {
        'vs_currency': vs_currency,
        'days': dias,
        'interval': intervalo
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        prices = pd.DataFrame(data['prices'], columns=["timestamp", "price"])
        prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')

        os.makedirs(output_path, exist_ok=True)
        caminho_saida = os.path.join(output_path, f"{ativo}_{intervalo}_{dias}d.csv")
        prices.to_csv(caminho_saida, index=False)
        print(f"✅ Dados salvos em: {caminho_saida}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao coletar dados de {ativo}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coleta de dados de criptomoedas via CoinGecko")
    parser.add_argument('--ativo', type=str, default='bitcoin', help='Nome do ativo (ex: bitcoin, ethereum)')
    parser.add_argument('--dias', type=int, default=30, help='Quantos dias de histórico')
    parser.add_argument('--intervalo', type=str, default='daily', choices=['minutely', 'hourly', 'daily'], help='Intervalo de dados')
    parser.add_argument('--saida', type=str, default='data/input', help='Diretório de saída')

    args = parser.parse_args()

    coletar_dados(
        ativo=args.ativo,
        dias=args.dias,
        intervalo=args.intervalo,
        output_path=args.saida
    )

def executar_coleta(ativo='bitcoin', dias=30, intervalo='daily', output_path='data/input'):
    coletar_dados(ativo=ativo, dias=dias, intervalo=intervalo, output_path=output_path)

