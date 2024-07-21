import uuid
from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select

from jose import jwt, JWTError
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token_schema import JwtTokenSchema, TokenPair
from app.schemas.user_schema import UserBase
from app.models.user import User
from app.models.blacklisted_model import BlacklistedToken
from app.services.hash import verify_password
from app.exceptions.http_exceptions import AuthFailedException
from app.database.connections import get_db
import logging

from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ACCESS_TOKEN_EXPIRES_MINUTES = 30
REFRESH_TOKEN_EXPIRES_MINUTES = 15 * 24 * 60  # 15 days


SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
httpBearer = HTTPBearer()

def _create_access_token(payload: dict, minutes: int | None = None) -> JwtTokenSchema:
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes or ACCESS_TOKEN_EXPIRES_MINUTES)

    payload[EXP] = expire

    token = JwtTokenSchema(token=jwt.encode(payload, settings.secret_key_jwt,
                           algorithm=settings.algorithm),
                           payload=payload, expire=expire)

    return token


def _create_refresh_token(payload: dict) -> JwtTokenSchema:
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)

    payload[EXP] = expire

    token = JwtTokenSchema(token=jwt.encode(payload, settings.secret_key_jwt, algorithm=settings.algorithm),
                           expire=expire,
                           payload=payload)

    return token


def create_token_pair(user: UserBase) -> TokenPair:
    payload = {SUB: str(user.email), JTI: str(uuid.uuid4()), IAT: datetime.now(timezone.utc)}

    return TokenPair(access=_create_access_token(payload={**payload}),
                     refresh=_create_refresh_token(payload={**payload}))


async def decode_access_token(token: str, db: AsyncSession):
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=[settings.algorithm])
        jti = payload.get(JTI)
        black_list_token = await BlacklistedToken.find_by_id(db=db, id=payload[JTI])
        if black_list_token:
            logger.info(f"Token {jti} is blacklisted")
            raise JWTError("Token is blacklisted")
    except JWTError as e:
        logger.error(f"JWT error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload


def refresh_token_state(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=[settings.algorithm])
    except JWTError:
        raise AuthFailedException()

    return {"token": _create_access_token(payload=payload).token}


def add_refresh_token_cookie(response: Response, token: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
    exp.replace(tzinfo=timezone.utc)

    response.set_cookie(
        key="refresh",
        value=token,
        expires=int(exp.timestamp()),
        httponly=True
    )

async def add_token_to_blacklist(token: str, db: AsyncSession = Depends(get_db)):

    try:
        
        payload = await decode_access_token(token=token, db=db)

        jti = payload.get(JTI)
        if jti is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
#        if await is_token_blacklisted(token=token, db=db):
#            raise AuthFailedException()


        black_listed = BlacklistedToken(id=payload[JTI], expire=datetime.fromtimestamp(payload[EXP], tz=timezone.utc))
    
        await black_listed.save(db=db)

        return {"msg": "Successfully logout"}
    except Exception as e:
        logger.error(f"Error adding token to blacklist: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have already log out!"
        )
        


#async def is_token_blacklisted(token: str, db: AsyncSession = Depends(get_db)):
#    payload = await decode_access_token(token=token, db=db)
#    
#    token_id = payload[JTI]

#    token_exist = await BlacklistedToken.find_by_id(id=str(token_id), db=db)

#    if token_exist is not None:
#        return True
#    return False


async def authenticate(email: str, password: str, db: AsyncSession):
    user = await User.find_by_email(db=db, email=email)
    if not user or not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

#    if await is_token_blacklisted(token, db):
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Token is blacklisted. Please log in again"
#        )
    print(token)
    try:
        payload = await decode_access_token(token=token, db=db)
        email = payload[SUB]
        if email is None:
            raise AuthFailedException()
    except JWTError as e:
        logger.error(f"Isuues in finding token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
   
    
    user = await User.find_by_email(email=email, db=db)
    if user is None:
        raise AuthFailedException()
    return user



def get_token_of_auth_user(credentials: HTTPAuthorizationCredentials = Depends(httpBearer)):
    token = credentials.credentials
    return token



