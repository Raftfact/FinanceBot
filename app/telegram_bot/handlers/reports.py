from aiogram import Router, types
from aiogram.filters import Command
router = Router()

@router.message(Command("report"))
async def cmd_report(message: types.Message):
    await message.answer("Здесь будет отчёт")