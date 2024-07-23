from fastapi_demo.orm.models.base import Base
from sqlalchemy import Column, String, BigInteger, Double, DateTime


class User(Base):
    __tablename__ = 'user_test'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
