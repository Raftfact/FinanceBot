from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.telegram_bot.states import TransactionStates
from app.services.transaction_service import create_transaction
from app.services.user_service import get_user
from decimal import Decimal


router = Router()


@router.message(Command("create_category"))
async def create(
    message: types.Message,
    state: FSMContext,
    db: AsyncSession
):
    user = await get_user(db, message.from_user.id, message.from_user.username)

    await state.update_data(
        user_id=user.id,
        is_creating_category=True
    )
    
    await message.answer("✏️ Введи название новой категории:")
    await state.set_state(TransactionStates.waiting_for_new_category)


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

    user_id = data.get("user_id")
    if user_id is None:
        user = await get_user(db, callback.from_user.id, callback.from_user.username)
        user_id = user.id
    
    is_creating_category = data.get("is_creating_category", False)
    
    if is_creating_category:
        await callback.message.answer(f"✅ Категория выбрана для использования!")
        await state.clear()
        await callback.answer()
        return
    
    amount = data.get("amount")
    comment = data.get("comment")
    operation = data.get("operation", "-")

    if amount is None:
        await callback.message.answer(f"✅ Категория выбрана!")
        await state.clear()
        await callback.answer()
        return

    transaction = await create_transaction(
        db=db,
        user_id=user_id,
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
    category_name = message.text.strip()
    
    if not category_name:
        await message.answer("❌ Название не может быть пустым. Попробуй ещё раз:")
        return
    
    user = await get_user(db, message.from_user.id, message.from_user.username)
    
    from app.services.category_service import create_category
    category = await create_category(db, category_name, user.id)
    
    await message.answer(f"✅ Категория '{category_name}' создана!")

    data = await state.get_data()
    is_creating_category = data.get("is_creating_category", False)
    
    if is_creating_category:
        await state.clear()
        return
    
    from app.services.category_service import get_categories, get_categories_keyboard
    categories = await get_categories(db, user.id)
    keyboard = get_categories_keyboard(categories)
    
    await message.answer("📂 Теперь выбери категорию:", reply_markup=keyboard)
    await state.set_state(TransactionStates.waiting_for_category)