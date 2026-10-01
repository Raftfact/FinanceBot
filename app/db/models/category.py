from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum
from app.core.database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False, default=TransactionType.EXPENSE)