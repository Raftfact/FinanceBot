from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.telegram_bot.states import TransactionStates
from app.services.transaction_service import create_transaction
from decimal import Decimal

router = Router()

@router.callback_query(F.data.startswith("cat_"))
async def handle_category_selection(
    callback: types.CallbackQuery, 
    state: FSMContext, 
    db: AsyncSession
):
    category_id = callback.data.replace("cat_", "")
    
    if category_id == "new":
        await callback.message.answer("✏️ Введи название новой категории:")
        await state.set_state(TransactionStates.waiting_for_new_category)
        await callback.answer()
        return
    
    data = await state.get_data()
    user_id = data["user_id"] 
    amount = Decimal(str(data["amount"]))
    comment = data["comment"]
    operation = data.get("operation", "")
    
    # Создаём транзакцию
    transaction = await create_transaction(
        db=db,
        user_id=user_id,  # ← РЕАЛЬНЫЙ user_id
        amount=amount,
        category_id=int(category_id),
        comment=f"{operation} {comment}",
        operation=operation
    )
    
    await callback.message.answer(f"✅ Записано: {operation}{amount} ₽ — {comment}")
    await state.clear()
    await callback.answer()

@router.message(TransactionStates.waiting_for_new_category)
async def handle_new_category_name(
    message: types.Message,
    state: FSMContext,
    db: AsyncSession
):
    """Обрабатывает ввод названия новой категории"""
    
    category_name = message.text.strip()
    
    if not category_name:
        await message.answer("❌ Название не может быть пустым. Попробуй ещё раз:")
        return
    
    # Получаем пользователя
    from app.services.user_service import get_user
    user = await get_user(db, message.from_user.id, message.from_user.username)
    
    # Создаём категорию
    from app.services.category_service import create_category
    category = await create_category(db, category_name, user.id)
    
    await message.answer(f"✅ Категория '{category_name}' создана!")
    
    # Возвращаемся к выбору категории
    from app.services.category_service import get_categories, get_categories_keyboard
    categories = await get_categories(db, user.id)
    keyboard = get_categories_keyboard(categories)
    
    await message.answer("📂 Теперь выбери категорию:", reply_markup=keyboard)
    await state.set_state(TransactionStates.waiting_for_category)