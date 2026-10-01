from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import get_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, db: AsyncSession):
    user = await get_user(db, message.from_user.id, message.from_user.username)
    await message.answer(f"Привет! Твой ID в системе: {user.id}")