from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: int
    password: str


class UserResp(UserBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True
