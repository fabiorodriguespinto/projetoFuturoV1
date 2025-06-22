##shared/telegram_bot.py

import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

ultimo_update_id = None

def enviar_mensagem(mensagem: str):
    try:
        url = f"{BASE_URL}/sendMessage"
        response = requests.post(url, json={"chat_id": CHAT_ID, "text": mensagem}, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Falha ao enviar mensagem para Telegram: {e}")

def escutar_comandos_telegram(ativo_monitorado: dict, scheduler):
    global ultimo_update_id
    print("🤖 Iniciando escuta de comandos via Telegram...")
    while True:
        try:
            params = {"timeout": 30}
            if ultimo_update_id:
                params["offset"] = ultimo_update_id + 1

            response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=60)
            response.raise_for_status()
            updates = response.json().get("result", [])

            for update in updates:
                ultimo_update_id = update["update_id"]
                message = update.get("message", {})
                texto = message.get("text", "").strip().lower()

                if not texto:
                    continue

                print(f"📨 Comando recebido: {texto}")
                if texto == "/parar":
                    if scheduler.running:
                        scheduler.pause()
                        enviar_mensagem("⏸️ Execução pausada.")
                elif texto == "/retomar":
                    if not scheduler.running:
                        scheduler.resume()
                        enviar_mensagem("▶️ Execução retomada.")
                elif texto.startswith("/ativo"):
                    partes = texto.split()
                    if len(partes) == 2:
                        ativo_monitorado["nome"] = partes[1]
                        enviar_mensagem(f"✅ Ativo alterado para: {partes[1]}")
                    else:
                        enviar_mensagem("⚠️ Uso correto: /ativo <nome_do_ativo>")
                elif texto == "/status":
                    status = "⏸️ Pausado" if not scheduler.running else "▶️ Executando"
                    enviar_mensagem(f"ℹ️ Ativo: {ativo_monitorado['nome']}\n⏱️ Status: {status}")
                else:
                    enviar_mensagem("❓ Comando não reconhecido. Use /status, /parar, /retomar ou /ativo <nome>.")

        except Exception as e:
            print(f"❌ Erro ao escutar comandos: {e}")
            time.sleep(5)
