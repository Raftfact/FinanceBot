import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.bot.handlers import start, transactions, reports


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(start.router)
    dp.include_router(transactions.router)
    dp.include_router(reports.router)
    
    print("🤖 Bot started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())