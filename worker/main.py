##worker/main.py

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from shared.market_data import coletar_candles_binance
from shared.database import SessionLocal
from shared.telegram_bot import enviar_mensagem, escutar_comandos_telegram
from shared.models import PredictionResult
from shared import config
import requests
import threading
import pytz


# =======================================================
# PREVISÃO VIA API FASTAPI
# =======================================================
def executar_inferencia():
    try:
        response = requests.post("http://api:8000/predict", timeout=10)
        result = response.json()
        return result.get("prediction"), result.get("models")
    except Exception as e:
        enviar_mensagem(f"❌ Erro na inferência: {e}")
        return None, {}


# =======================================================
# GRAVAR PREVISÃO NO POSTGRES
# =======================================================
def registrar_previsao(valor_previsto: float):
    db = SessionLocal()
    registro = PredictionResult(
        timestamp=datetime.utcnow(),
        predicted_price=valor_previsto,
        strategy_signal="",
        model_used="ensemble"
    )
    db.add(registro)
    db.commit()
    db.close()


# =======================================================
# SIMULAÇÃO DE OPERAÇÃO (ESTRATÉGIA)
# =======================================================
def simular_operacao(preco_real: float, previsao: float) -> str:
    margem = 0.01  # 1%

    if previsao > preco_real * (1 + margem):
        return "COMPRA"
    elif previsao < preco_real * (1 - margem):
        return "VENDA"
    return "HOLD"


# =======================================================
# REGISTRAR OPERAÇÃO NO POSTGRES
# =======================================================
def registrar_operacao(tipo: str, preco_real: float, previsao: float):
    db = SessionLocal()
    resultado = ((previsao - preco_real) / preco_real) * 100

    registro = PredictionResult(
        timestamp=datetime.utcnow(),
        predicted_price=previsao,
        strategy_signal=tipo,
        model_used=f"variação: {resultado:.2f}%"
    )
    db.add(registro)
    db.commit()
    db.close()


# =======================================================
# EXECUTAR TODA A ANÁLISE (FLUXO PRINCIPAL)
# =======================================================
def realizar_analise():
    enviar_mensagem("⏱ Iniciando análise...")

    # 1) Coletar dados da Binance
    try:
        coletar_candles_binance()
    except Exception as e:
        enviar_mensagem(f"❌ Erro na coleta: {e}")
        return

    # 2) Inferência via API
    previsao, detalhes = executar_inferencia()
    if previsao is None:
        return

    # 3) Preço real = último candle recebido (pegar do banco)
    from shared.market_data import carregar_candles
    df = carregar_candles(limit=1)
    preco_real = float(df["close"].iloc[-1])

    # 4) Estratégia
    tipo_operacao = simular_operacao(preco_real, previsao)

    # 5) Registrar resultados
    registrar_previsao(previsao)
    registrar_operacao(tipo_operacao, preco_real, previsao)

    # 6) Envio Telegram
    msg = (
        f"📈 Execução concluída.\n"
        f"📉 Real: {preco_real:.2f}\n"
        f"🔮 Previsão: {previsao:.2f}\n\n"
        f"🧠 Detalhes por modelo:\n" +
        "\n".join([f"• {k}: {v:.2f}" for k, v in detalhes.items()]) +
        f"\n\n💡 Operação sugerida: {tipo_operacao}"
    )
    enviar_mensagem(msg)


# =======================================================
# CALLBACK PARA COMANDOS DO TELEGRAM
# =======================================================
def executar_callback():
    realizar_analise()


# =======================================================
# INICIAR SCHEDULER E LISTENER
# =======================================================
if __name__ == "__main__":
    ativo_monitorado = "bitcoin"

    timezone = pytz.timezone("America/Sao_Paulo")
    scheduler = BlockingScheduler(timezone=timezone)
    scheduler.add_job(realizar_analise, "interval", minutes=2)

    thread = threading.Thread(
        target=escutar_comandos_telegram,
        args=(ativo_monitorado, scheduler, executar_callback)
    )
    thread.daemon = True
    thread.start()

    enviar_mensagem("🤖 Worker iniciado e aguardando rotinas...")

    scheduler.start()
