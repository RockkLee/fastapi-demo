from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi_demo.api.schemas.user import UserCreate, UserResp
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
