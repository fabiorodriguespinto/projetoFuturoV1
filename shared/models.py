# shared/models.py

from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from shared.database import Base


class Candle(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True)
    open_time = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    predicted_price = Column(Float)
    strategy_signal = Column(String)
    model_used = Column(String)


