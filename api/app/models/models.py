from sqlalchemy import Column, Integer, Float, DateTime
from app.services.database import Base
from datetime import datetime

class PredictionResult(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    #price = Column(Float)
    #day_of_year = Column(Integer)
    #created_at = Column(DateTime, default=datetime.utcnow)
    symbol = Column(String)
    prediction = Column(Float)