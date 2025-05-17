from sqlalchemy import Column, Integer, String, Float
from app.services.database import Base

class TradeModel(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    prediction = Column(Float)
