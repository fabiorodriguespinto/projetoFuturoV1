FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências Python (incluindo APScheduler no requirements.txt)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Executa o script Python principal diretamente (que deverá usar o APScheduler para agendamento)
CMD ["python", "main.py"]
