from datetime import datetime
from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from sqlalchemy import delete

from fastapi_demo.api.schemas.user import UserCreate
from fastapi_demo.orm.connection import async_session, engine
from fastapi_demo.orm.models.user import User
from fastapi_demo.services.user_service import UserService


class TestUserService(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):  # This method is called before each test
        print("******** TestUserService.setUp()")
        self.mockdb = AsyncMock()
        self.db = async_session()
        self.engine = engine

    async def asyncTearDown(self):  # This method is called after each test
        print("******** TestUserService.tearDown()")
        await self.db.close()  # Return the connection to the connection pool within the Engine, not actually close.
        await self.engine.dispose()  # Close all connections in the connection pool

    async def test_create_user(self):
        try:
            sql_delete = delete(User).where(User.username == "aaa123")
            await self.db.execute(sql_delete)
            await self.db.commit()

            user_service = UserService(self.db)
            new_user = await user_service.create_user(
                UserCreate(username="aaa123", password="bbb456")
            )
            self.assertEqual(new_user.username, "aaa123")
            self.assertEqual(new_user.password, "bbb456")
        finally:
            sql_delete = delete(User).where(User.username == "aaa123")
            await self.db.execute(sql_delete)
            await self.db.commit()

    async def test_get_user_mock(self):
        user_id = 1
        # mock the dao inside the service
        user_service = UserService(self.mockdb)
        user_service.user_dao.get_user_by_id = AsyncMock(
            return_value=User(id=user_id, username="aaa123", password="bbb456", create_date=datetime.now())
        )

        result = await user_service.get_user_by_id(user_id)
        print(result.__dict__)
        self.assertEqual(type(result), User)
        self.assertEqual(result.id, user_id)
        self.assertEqual(result.username, "aaa123")
        self.assertEqual(result.password, "bbb456")
