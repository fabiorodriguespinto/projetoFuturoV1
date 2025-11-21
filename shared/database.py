# shared/database.py

import os
import pandas as pd
from sqlalchemy import create_engine, text, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------
# Configurações do Banco
# ------------------------------
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "futuro")
DB_HOST = os.getenv("DB_HOST", "postgres")  # O nome do serviço no docker-compose
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ------------------------------
# Modelo da tabela CANDLES
# ------------------------------
class Candle(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


# ------------------------------
# Criar tabelas se não existirem
# ------------------------------
def init_db():
    Base.metadata.create_all(bind=engine)


# ------------------------------
# Função usada pela API /predict
# ------------------------------
def carregar_candles(limit=100):
    """Carrega candles do PostgreSQL e retorna um DataFrame."""
    with SessionLocal() as session:
        sql = text("""
            SELECT timestamp, open, high, low, close, volume
            FROM candles
            ORDER BY timestamp DESC
            LIMIT :limit
        """)

        rows = session.execute(sql, {"limit": limit}).fetchall()

        if not rows:
            return None

        df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df.sort_values("timestamp", inplace=True)
        return df

