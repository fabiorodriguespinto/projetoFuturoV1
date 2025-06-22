# test_telegram.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

message = "🚀 Teste de envio via Telegram bot."

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})

print("Status:", response.status_code)
print(response.text)

