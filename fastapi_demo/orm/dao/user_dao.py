from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_demo.orm.models.user import User  # Ensure this path matches your User model location


class UserDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: User) -> User:
        # user_data = user.dict()
        # new_user = User(**user_data)
        self.db.add(user)
        return user

    async def get_user_by_id(self, id: int) -> User:
        stmt = select(User).where(User.id == id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def update_user_by_id(self, user: User):
        stmt = (
            update(User)
            .where(User.id == int(user.id))
            .values(username=user.username, password=user.password, create_date=datetime.now())
        )
        await self.db.execute(stmt)

    async def delete_user_by_id(self, id: int):
        stmt = delete(User).where(User.id == id)
        await self.db.execute(stmt)
