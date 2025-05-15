FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pandas requests

# Instala o cron
RUN apt-get update && apt-get install -y cron

# Copia o arquivo de agendamento
COPY cronjob /etc/cron.d/cronjob

# Dá permissão e ativa o agendamento
RUN chmod 0644 /etc/cron.d/cronjob && crontab /etc/cron.d/cronjob

# Executa o cron em primeiro plano
CMD ["cron", "-f"]
