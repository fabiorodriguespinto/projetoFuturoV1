import pytest
from worker.main import coletar_dados, processar_dados
from shared.notifications import notificar_telegram

# Teste 1: coleta de dados deve retornar uma lista de dicts válidos
def test_coletar_dados_retorna_dados_validos():
    dados = coletar_dados()
    
    assert isinstance(dados, list)
    assert len(dados) > 0
    for item in dados:
        assert isinstance(item, dict)
        assert "preco" in item
        assert "timestamp" in item

# Teste 2: processamento de dados com entrada vazia
def test_processar_dados_com_lista_vazia():
    resultado = processar_dados([])
    
    assert resultado is None or resultado == {}

# Teste 3: simula envio de notificação para o Telegram com requests-mock
def test_notificar_telegram_sucesso(requests_mock):
    telegram_api_url = "https://api.telegram.org/bot123456:ABC/sendMessage"
    mock_response = {"ok": True, "result": {"message_id": 1}}

    requests_mock.post(telegram_api_url, json=mock_response)

    # Substitua TOKEN e CHAT_ID com os do .env ou mockados no código
    response = notificar_telegram("Mensagem de teste", bot_token="123456:ABC", chat_id="999999")

    assert response["ok"] is True
