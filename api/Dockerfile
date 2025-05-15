FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação e o requirements.txt
#COPY . .

COPY ./app /app/app
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]