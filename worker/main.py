##worker/main.py

import sqlite3
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from tasks.retrain_model import executar_retreinamento
from tasks.coleta_cripto import executar_coleta
import requests
from shared.telegram_bot import enviar_mensagem
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import threading
from shared.telegram_bot import enviar_mensagem, escutar_comandos_telegram

def coletar_e_salvar_dados():
    executar_coleta(ativo="bitcoin", dias=30, intervalo="daily", output_path="/data/input")

def executar_inferencia():
    try:
        response = requests.post("http://api:8000/predict", json={"input_data": "exemplo"}, timeout=10)
        response.raise_for_status()
        prediction = response.json()
        return prediction.get("prediction", 0.0)
    except Exception as e:
        print(f"❌ Erro na inferência: {e}")
        return -1.0

def registrar_previsao(price: float):
    day_of_year = datetime.now().timetuple().tm_yday
    conn = sqlite3.connect("/data/app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price REAL,
            day_of_year INT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO predictions (price, day_of_year, created_at)
        VALUES (?, ?, ?)
    """, (price, day_of_year, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def realizar_analise():
    print("🟢 Início da análise programada")
    coletar_e_salvar_dados()
    price = executar_inferencia()
    registrar_previsao(price)
    executar_retreinamento()
    print(f"Preço previsto: {price}")
    enviar_mensagem(f"📈 Execução concluída. Preço estimado: ${price:.2f}")
    print("✅ Análise concluída e notificação enviada")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    #scheduler.add_job(realizar_analise, 'interval', hours=1)
    scheduler.add_job(realizar_analise, 'interval', minutes=1)
    print("🚀 Scheduler iniciado. Executando a cada 1 hora...")

    # Inicia o listener do Telegram em uma thread separada
    ativo_monitorado = {"nome": "bitcoin"}  # Pode ser alterado via comando Telegram
    #thread = threading.Thread(target=escutar_comandos_telegram, args=(ativo_monitorado, scheduler))
    thread = threading.Thread(
    target=escutar_comandos_telegram,
    args=(ativo_monitorado, scheduler, realizar_analise)
    )
    thread.daemon = True
    thread.start()

    #realizar_analise()  # Executa na inicialização - Comentada para evitar mensagens duplicadas no telegram
    scheduler.start()