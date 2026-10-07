from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.transaction import Transaction
from app.services.user_service import update_balance
from decimal import Decimal
from sqlalchemy import extract, select, func
from app.db.models.category import Category

async def create_transaction(
    db: AsyncSession,
    user_id: int,
    amount: Decimal,
    category_id: int,
    comment: str,
    operation: str = "-"
):
    transaction = Transaction(
            user_id= user_id,
            category_id= category_id,
            amount = amount,
            comment = comment
        )
        
    db.add(transaction)
    await db.flush()

    if operation == "+":
        await update_balance(db, user_id, amount)
    else:
        await update_balance(db, user_id, -amount)
        
    return transaction

async def get_monthly_report(db: AsyncSession, user_id: int, year: int, month: int):
    result = await db.execute(
        select(
            Category.name,
            Category.type,
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count")
        )
        .join(Category, Transaction.category_id == Category.id)
        .where(
            Transaction.user_id == user_id,
            extract('year', Transaction.transaction_date) == year,
            extract('month', Transaction.transaction_date) == month
        )
        .group_by(Category.name, Category.type)
        .order_by(func.sum(Transaction.amount).desc())
    )
    return result.all()