import uuid
from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token_schema import JwtTokenSchema, TokenPair
from app.schemas.user_schema import User
from app.models.blacklisted_model import BlacklistedToken
from app.exceptions.http_exceptions import AuthFailedException

from app.config import settings


ACCESS_TOKEN_EXPIRES_MINUTES = 30
REFRESH_TOKEN_EXPIRES_MINUTES = 15 * 24 * 60  # 15 days


SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"


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


def create_token_pair(user: User) -> TokenPair:
    payload = {SUB: str(user.id), JTI: str(uuid.uuid4()), IAT: datetime.now(timezone.utc)}

    return TokenPair(access=_create_access_token(payload={**payload}),
                     refresh=_create_refresh_token(payload={**payload}))


async def decode_access_token(token: str, db: AsyncSession):
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=[settings.algorithm])
        black_list_token = await BlacklistedToken.find_by_id(db=db, id=payload[JTI])
        if black_list_token:
            raise JWTError("Token is blacklisted")
    except JWTError:
        raise AuthFailedException()

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




