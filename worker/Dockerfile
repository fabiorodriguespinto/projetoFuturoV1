##worker/Dockerfile
# Dockerfile da WORKER

FROM python:3.11

WORKDIR /worker

# Copia apenas arquivos do worker sem sobrescrever o shared
COPY worker/main.py /worker/main.py
COPY worker/requirements.txt /worker/requirements.txt
COPY worker/market_collector.py /worker/market_collector.py
COPY worker/tasks /worker/tasks

# Copia shared corretamente
COPY shared /worker/shared

# Copia a neural_network
COPY neural_network /worker/neural_network

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/worker"

CMD ["python", "main.py"]

