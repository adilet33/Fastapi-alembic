from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database.connections import get_db
from app.schemas.user_schema import UserResponse, UserCreate
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user import create_user, create_token_for_user
from app.services.auth import add_token_to_blacklist
from app.services.auth import get_current_user, get_token_of_auth_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(body=user, db=db)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    access_token = await create_token_for_user(body=body, db=db,) #response=Response)

    return access_token


@router.post("/logout", status_code=status.HTTP_200_OK)
async  def logout(token: str = Depends(get_token_of_auth_user), db: AsyncSession = Depends(get_db)):
    #logger.info(f"Token received for logout: {token}")
    return await add_token_to_blacklist(token=token, db=db)


@router.get("/protected_data")
async def read_user(user: User = Depends(get_current_user)):
    return {f"This is protected data and available for {user.email}"}









    


