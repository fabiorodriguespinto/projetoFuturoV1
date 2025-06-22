import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN ou CHAT_ID não definidos no arquivo .env")

URL_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Enviar mensagem simples
def enviar_mensagem(mensagem: str):
    try:
        url = f"{URL_BASE}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": mensagem
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

# Escutar comandos via long polling
def escutar_comandos_telegram(ativo_monitorado, scheduler, executar_callback):
    print("🔁 Escutando comandos do Telegram...")
    offset = None

    while True:
        try:
            params = {"timeout": 10, "offset": offset}
            resp = requests.get(f"{URL_BASE}/getUpdates", params=params, timeout=15)
            resp.raise_for_status()
            updates = resp.json()

            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                mensagem = update.get("message", {})
                chat_id = str(mensagem.get("chat", {}).get("id", ""))
                texto = mensagem.get("text", "").strip()

                # Ignorar mensagens de outros usuários
                if chat_id != CHAT_ID:
                    continue

                if texto.lower() == "/status":
                    enviar_mensagem(f"🤖 Bot ativo. Monitorando {ativo_monitorado['nome']}.")
                elif texto.startswith("/alterar"):
                    partes = texto.split()
                    if len(partes) == 2:
                        ativo_monitorado["nome"] = partes[1]
                        enviar_mensagem(f"🔄 Ativo alterado para: {ativo_monitorado['nome']}")
                    else:
                        enviar_mensagem("❌ Formato inválido. Use: /alterar bitcoin")
                elif texto.lower() == "/executar":
                    enviar_mensagem("⏱ Executando análise manual agora...")
                    executar_callback()  # Chamada direta para função de execução
                else:
                    enviar_mensagem("🤖 Comando não reconhecido. Use /status ou /alterar <ativo>.")

        except Exception as e:
            print(f"❌ Erro no polling do Telegram: {e}")
            time.sleep(5)  # Espera e tenta de novo
