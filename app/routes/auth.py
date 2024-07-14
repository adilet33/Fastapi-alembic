from fastapi import APIRouter, Depends, status
from app.database.connections import get_db
from app.schemas.user_schema import UserResponse, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user import create_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(body=user, db=db)
    return new_user




