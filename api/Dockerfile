##api/Dockerfile
# Dockerfile da API

FROM python:3.11-slim

# Variáveis de ambiente recomendadas
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação
COPY api/app /app/app

# ⚠️ Copia também a pasta nn (necessário para importar nn.inference.predict)
COPY nn /app/nn

# Copia o requirements.txt
COPY api/requirements_api.txt .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_api.txt

# Expõe a porta da API
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

