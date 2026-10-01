from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User

async def find_user(db: AsyncSession, telegram_id: int):

    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    return user

async def create_user(db: AsyncSession, telegram_id: int, username: str):
    user = User(
    telegram_id=telegram_id,            
    username=username
    )
    db.add(user)
    await db.flush()
    
    return user

async def get_user(db: AsyncSession, user_id: int, username = None):
    find_us = await find_user(db, user_id)
    if find_us is None:
        return await create_user(db, user_id, username)
    elif find_us is not None: 
        return find_us