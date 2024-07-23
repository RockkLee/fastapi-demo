from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response

from fastapi_demo.api.schemas.msg import MsgResp
from fastapi_demo.api.schemas.user import UserCreate, UserResp, UserUpdate
from fastapi_demo.orm.connection import get_session
from fastapi_demo.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=['user_api']
)


@router.post("/create/", response_model=UserResp, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)

    created_user = await user_service.create_user(user)
    return created_user


@router.get("/get/{user_id}", response_model=UserResp)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)

    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/update", response_model=MsgResp, status_code=status.HTTP_200_OK)
async def update_user(user: UserUpdate, db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)

    if not await user_service.get_user_by_id(user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await user_service.update_user_by_id(user)
    return MsgResp("The user has been updated")


@router.delete("/delete/{user_id}", response_model=MsgResp, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)

    if not await user_service.get_user_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await user_service.delete_user_by_id(user_id)
    return MsgResp("The user has been deleted")
