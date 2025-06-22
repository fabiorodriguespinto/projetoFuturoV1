import requests
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

r = requests.get(url)
print(r.status_code)
print(r.json())
