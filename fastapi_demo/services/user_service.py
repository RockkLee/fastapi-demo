from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_demo.api.schemas.user import UserCreate
from fastapi_demo.orm.dao.user_dao import UserDAO
from fastapi_demo.orm.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_dao = UserDAO(db)

    async def create_user(self, user: UserCreate):
        created_user = await self.user_dao.create_user(
            User(username=user.username, password=user.password, create_date=datetime.now())
        )
        return created_user

    async def get_user_by_id(self, id: int):
        return await self.user_dao.get_user_by_id(id)

    async def update_user_by_id(self, user: UserCreate):
        return await self.user_dao.update_user_by_id(
            User(id=user.id, username=user.username, password=user.password, create_date=datetime.now())
        )

    async def delete_user_by_id(self, id: int):
        return await self.user_dao.delete_user_by_id(id)