from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.db.models.category import Category

async def create_category(db: AsyncSession, category_name: str, user_id: int):
    category = Category(
        name=category_name,
        user_id=user_id
    )
    db.add(category)
    await db.flush()
    
    return category

async def get_categories(db: AsyncSession, user_id: int):
    query = select(Category).where(Category.user_id == user_id)
    result = await db.execute(query)
    categorys = result.scalars().all()
    
    return categorys

def get_categories_keyboard(categories):
    keyboard = []
    for cat in categories:
        button = InlineKeyboardButton(
            text=cat.name,
            callback_data=f"cat_{cat.id}"
        )
        keyboard.append([button])
    
    keyboard.append([
        InlineKeyboardButton(text="➕ Создать новую", callback_data="cat_new")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def edit_category(db: AsyncSession, category_name: str, user_id: int):
    pass

async def remove_category(db: AsyncSession, category_name: str, user_id: int):
    pass