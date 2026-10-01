from aiogram import Router, types
from aiogram.filters import Command
router = Router()

@router.message(Command("transaction"))
async def handle_transaction(message: types.Message):
    await message.answer("Эта команда пока не готова!")