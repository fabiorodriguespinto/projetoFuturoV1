# init/Dockerfile

FROM python:3.11

WORKDIR /init

COPY init /init
COPY shared /init/shared
COPY neural_network /init/neural_network

COPY init/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/init"

CMD ["python", "db_init.py"]
