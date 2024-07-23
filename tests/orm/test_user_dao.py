from datetime import datetime
from typing import Optional
from unittest import TestCase, IsolatedAsyncioTestCase
from sqlalchemy import delete, select

from fastapi_demo.orm.connection import async_session, engine
from fastapi_demo.orm.dao.user_dao import UserDAO
from fastapi_demo.orm.models.user import User


# Can not use `async with async_session() as db:` to create a session in each test function.
# It works if we run the test functions separately,
# but it will fail if we run all test functions together.
# It is because running unittest functions all together uses only one process.
class TestUserDAO(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):  # This method is called before each test
        print("******** TestUserDAO.setUp()")
        self.db = async_session()
        self.engine = engine

    async def asyncTearDown(self):  # This method is called after each test
        print("******** TestUserDAO.tearDown()")
        await self.db.close()  # Return the connection to the connection pool within the Engine, not actually close.
        await self.engine.dispose()  # Close all connections in the connection pool

    async def test_create_user(self):
        sql_delete = delete(User).where(User.username == "aaa123")
        await self.db.execute(sql_delete)
        await self.db.commit()

        user_dao = UserDAO(self.db)
        new_user = await user_dao.create_user(
            User(username="aaa123", password="bbb456", create_date=datetime.now())
        )
        self.assertNotEqual(new_user, None)

    async def test_get_user_by_id(self):
        user_dao = UserDAO(self.db)
        # create a row of test data
        user = User(username="aaa123", password="bbb456", create_date=datetime.now())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        user_id = int(user.id)
        print(f"added_user.id: {user_id}")
        try:
            # search
            user = await user_dao.get_user_by_id(user_id)
            print(f"searched_user: {user.__dict__}")
            self.assertEqual(type(user), User)
        except Exception as e:
            await self.db.rollback()
            raise e
        finally:
            sql_delete = delete(User).where(User.id == user_id)
            await self.db.execute(sql_delete)
            await self.db.commit()

    async def test_update_user_by_id(self):
        user_dao = UserDAO(self.db)
        # create a row of test data
        user = User(username="aaa123", password="bbb456", create_date=datetime.now())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        user_id = int(user.id)
        print(f"added_user.id: {user_id}")
        try:
            # update
            await user_dao.update_user_by_id(
                User(id=user_id, username="aaa123", password="test123", create_date=datetime.now())
            )
            await self.db.commit()

            # check if the update function works
            stmt = select(User).where(User.id == user_id)
            result = await self.db.execute(stmt)
            result = result.scalar()
            print(f"updated_user: {result.__dict__}")
            self.assertEqual(type(user), User)
            self.assertEqual(result.username, "aaa123")
            self.assertEqual(result.password, "test123")
        except Exception as e:
            await self.db.rollback()
            raise e
        finally:
            sql_delete = delete(User).where(User.id == user_id)
            await self.db.execute(sql_delete)
            await self.db.commit()

    async def test_delete_user_by_id(self):
        user_dao = UserDAO(self.db)
        user_id = 0
        try:
            # create a row of test data
            user = User(username="aaa123", password="bbb456", create_date=datetime.now())
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            user_id = int(user.id)
            print(f"added_user.id: {user_id}")
        except Exception as e:
            await self.db.rollback()
            raise e
        finally:
            # check if the data has been created
            stmt = select(User).where(User.id == user_id)
            result = await self.db.execute(stmt)
            self.assertEqual(type(result.scalar()), User)

            self.assertNotEqual(user_id, 0)
            await user_dao.delete_user_by_id(user_id)
            await self.db.commit()

            # check if the delete function works
            stmt = select(User).where(User.id == user_id)
            result = await self.db.execute(stmt)
            self.assertEqual(result.scalar(), None)