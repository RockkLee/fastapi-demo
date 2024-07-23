from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True
