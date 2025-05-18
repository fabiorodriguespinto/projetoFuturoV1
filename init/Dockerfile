FROM python:3.10-slim

WORKDIR /app

COPY db_init.py .

# Copie o requirements.txt se o script tiver dependências
# COPY ../api/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Se o db_init.py for autossuficiente (ex: usa apenas sqlite3), isso basta:
CMD ["python", "db_init.py"]
