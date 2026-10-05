from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Numeric, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    timezone = Column(String, default="UTC")
    balance = Column(Numeric(precision=15, scale=2), server_default='0', default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())