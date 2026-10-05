from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_category(db: AsyncSession, category_name: str, user_id: int):
    category = Category(
        category_name=category_name,
        user_id=user_id
    )
    db.add(category)
    await db.flush()
    
    return category

async def get_categorys(db: AsyncSession, user_id: int):
    query = select(Category).where(Category.user_id == user_id)
    result = await db.execute(query)
    categorys = result.scalars().all()
    
    return categorys