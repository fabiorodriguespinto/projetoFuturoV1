import os
from dotenv import load_dotenv

# Carrega variáveis do .env na raiz
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def notificar_telegram(mensagem: str):
    import requests
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN ou CHAT_ID não configurados")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
