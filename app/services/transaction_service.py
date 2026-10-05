from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.transaction import Transaction
from app.services.user_service import update_balance
from decimal import Decimal

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