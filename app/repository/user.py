from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connections import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.models.user import User
from app.services.hash import get_password_hash


async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user_exists = await User.find_by_email(email=body.email, db=db)
    
    if user_exists is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email is already exist")
    
    username_exists = await User.find_by_username(username=body.username, db=db)
    
    if username_exists is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"username {body.username} is already exist. Choose another username")

    user_data = body.model_dump(exclude={"password_confirm"})
    user_data["password"] = get_password_hash(user_data["password"])

    new_user = User(**user_data)
    await new_user.save(db=db)

    new_user_dict = {
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'age': new_user.age,
        'email': new_user.email
    }

    response_user = UserResponse.model_validate(new_user_dict)

    return response_user




