from aiogram import Router, types
from datetime import datetime
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.transaction_service import get_monthly_report
from app.services.user_service import get_user
from app.db.models.category import TransactionType

router = Router()

@router.message(Command("report"))
async def cmd_report(message: types.Message, db: AsyncSession):
    user = await get_user(db, message.from_user.id)
    if not user:
        await message.answer("Сначала используй /start")
        return
    
    now = datetime.utcnow()
    report = await get_monthly_report(db, user.id, now.year, now.month)
    
    if not report:
        await message.answer("📊 В этом месяце еще нет записей")
        return
    
    total_income = sum(r.total for r in report if r.type == TransactionType.INCOME)
    total_expense = sum(r.total for r in report if r.type == TransactionType.EXPENSE)
    
    text = f"📊 *Отчет за {now.strftime('%B %Y')}*\n\n"
    
    if total_income > 0:
        text += f"💰 *Доходы:* {total_income} ₽\n"
        for r in report:
            if r.type == TransactionType.INCOME:
                text += f"  • {r.name}: {r.total} ₽ ({r.count} шт.)\n"
        text += "\n"
    
    if total_expense > 0:
        text += f"💸 *Расходы:* {total_expense} ₽\n"
        for r in report:
            if r.type == TransactionType.EXPENSE:
                text += f"  • {r.name}: {r.total} ₽ ({r.count} шт.)\n"
        text += "\n"
    
    balance = total_income - total_expense
    text += f"💎 *Баланс:* {balance} ₽"
    
    await message.answer(text, parse_mode="Markdown")