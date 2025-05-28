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


#ESte ou o código acima
# shared/notifications.py

#import os
#import requests

#def notificar_telegram(mensagem, bot_token=None, chat_id=None):
#    bot_token = bot_token or os.getenv("BOT_TOKEN")
#    chat_id = chat_id or os.getenv("CHAT_ID")

#    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#    payload = {
#        "chat_id": chat_id,
#        "text": mensagem
#    }

#    response = requests.post(url, json=payload)
#    return response.json()

