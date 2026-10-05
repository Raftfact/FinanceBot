from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.telegram_bot.states import TransactionStates
from app.services.parser_service import parse_transaction_message
from app.services.category_service import get_categories_keyboard, get_categories
from app.services.user_service import get_user

router = Router()

@router.message(F.text.regexp(r'^[+-]?\d'))
async def process_transaction_input(
    message: types.Message,
    state: FSMContext, 
    db: AsyncSession
):
    user = await get_user(db, message.from_user.id, message.from_user.username)
    categories = await get_categories(db, user.id)
    parsed = parse_transaction_message(message.text)
    
    if parsed is None:
        await message.answer("❌ Не понял формат. Напиши: сумма описание\nНапример: (+/-)450 кофе")
        return
    
    await state.update_data(
        amount=parsed["amount"],
        comment=parsed["comment"],
        operation=parsed["operation"],
        user_id=user.id
    )
    
    await state.set_state(TransactionStates.waiting_for_category)

    keyboard = get_categories_keyboard(categories)
    
    await message.answer(f"📝 Записываю: {parsed['operation']} {parsed['amount']} ₽ — {parsed['comment']}\n\nВыбери категорию:", reply_markup=keyboard)