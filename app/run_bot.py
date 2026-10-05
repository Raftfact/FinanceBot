from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.core.config import settings
from app.telegram_bot.handlers.start import router as start_router
from app.telegram_bot.handlers.transactions import router as transactions_router
from app.telegram_bot.handlers.reports import router as reports_router
from app.telegram_bot.handlers.categories import router as categories_router
from app.telegram_bot.middlewares.db_session import DbSessionMiddleware


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DbSessionMiddleware())

    dp.include_router(start_router)
    dp.include_router(transactions_router)
    dp.include_router(reports_router)
    dp.include_router(categories_router)
    
    print("🤖 Bot started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())