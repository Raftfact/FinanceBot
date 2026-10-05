from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.telegram_bot.states import TransactionStates
from app.services.parser_service import parse_transaction_message

router = Router()

@router.message()
async def process_transaction_input(
    message: types.Message, 
    state: FSMContext, 
    db: AsyncSession
):
    parsed = parse_transaction_message(message.text)
    
    if parsed is None:
        await message.answer("❌ Не понял формат. Напиши: сумма описание\nНапример: (+/-)450 кофе")
        return
    
    await state.update_data(
        amount=parsed["amount"],
        comment=parsed["comment"],
        operation=parsed["operation"]
    )
    
    await state.set_state(TransactionStates.waiting_for_category)
    
    await message.answer(f"📝 Записываю: {parsed['operation']} {parsed['amount']} ₽ — {parsed['comment']}\n\nВыбери категорию:")