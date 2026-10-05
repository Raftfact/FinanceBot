from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import get_user, get_balance

router = Router()

help_message = (
    "Вот что я умею:\n"
    "- Записываю доходы и расходы\n"
    "- Создаю категории расходов\n"
    "- Формирую отчёты по расходам\n\n"
    "Чтобы записать транзакцию, просто напиши её в формате:\n"
    "<+/-> <сумма> <описание>\n"
    "Например: +450 кофе или -200 транспорт\n\n"
    "Чтобы создать категорию, используй команду /create_category <название категории>\n"
    "Или создай категорию прямо в процессе записи транзакции, когда я спрошу про категорию.\n\n"
    "Чтобы получить отчёт, используй команду /report\n\n"
    "Если нужна помощь, напиши /help."
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message, db: AsyncSession):
    user = await get_user(db, message.from_user.id, message.from_user.username)
    await message.answer(f"Привет {user.username}! \n\n{help_message}")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(help_message)

@router.message(Command("balance"))
async def cmd_balance(message: types.Message, db: AsyncSession):
    user = await get_user(db, message.from_user.id, message.from_user.username)
    balance = await get_balance(db, user.id)
    await message.answer(f"Ваш общий баланс: {balance}")