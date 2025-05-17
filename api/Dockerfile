FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação
COPY ./app /app/app

# Copia o requirements.txt
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
