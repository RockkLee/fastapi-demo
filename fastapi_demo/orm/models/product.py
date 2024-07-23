from fastapi_demo.orm.models.base import Base
from sqlalchemy import Column, String, BigInteger, Double, DateTime


class Product(Base):
    __tablename__ = 'product_test'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    create_date = Column(DateTime, nullable=False)
