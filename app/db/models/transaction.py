from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    comment = Column(String, nullable=True)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="transactions")
    category = relationship("Category", backref="transactions")