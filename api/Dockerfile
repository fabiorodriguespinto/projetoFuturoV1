##api/Dockerfile
# Dockerfile da API

FROM python:3.11

WORKDIR /app

# instalar dependências
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar código
COPY api/app /app/app
COPY shared /app/shared
COPY neural_network /app/neural_network

# garantir que shared e neural_network sejam encontráveis
ENV PYTHONPATH="/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

