import sqlite3
import os

# Caminho do banco de dados — deve coincidir com o volume mapeado em docker-compose
DB_PATH = "/app/data/trades.db"

# Criação da pasta se não existir (caso esteja em volume compartilhado)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Conecta (cria o arquivo se ainda não existir)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Cria tabela de forma idempotente
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    timestamp TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print(f"Banco inicializado em: {DB_PATH}")

