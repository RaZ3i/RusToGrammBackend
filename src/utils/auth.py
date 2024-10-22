import datetime
from datetime import timedelta
from typing import Annotated
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from starlette import status

from src.service.service import validate_password
from src.schemas.user_info import UserInfo
from src.config import settings
from src.service.service import get_user_auth_info, get_user_data

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(
    payload: dict,
    private_key=settings.PRIVATE_KEY_PATH.read_text(),
    algorithm=settings.ALGORITHM,
    expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str,
    pulblic_key=settings.PUBLIC_KEY_PATH.read_text(),
    algoritm=settings.ALGORITHM,
):
    decoded = jwt.decode(token, pulblic_key, algorithms=[algoritm])
    return decoded


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserInfo) -> str:
    jwt_payload = {
        "sub": user["login"],
        "id": user["id"],
        "login": user["login"],
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: UserInfo) -> str:
    jwt_payload = {"sub": user["login"]}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


async def validate_auth_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль или логин"
    )
    try:
        user = await get_user_auth_info(user_data.username)
        user_hash_pass = user["password"]
        if validate_password(user_data.password, user_hash_pass):
            return user
        else:
            raise unauthed_exc
    except:
        raise unauthed_exc


async def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(ouath2_scheme),
) -> UserInfo:
    # token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type"
    )


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserInfo:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    user_login: str | None = payload.get("login")
    try:
        user = await get_user_data(user_login=user_login)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )
    return user


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
):
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    user_login: str | None = payload.get("sub")
    try:
        user = await get_user_data(user_login=user_login)
        user_info = {"login": user.login, "id": user.id, "phone": user.phone}
        # print(user_info)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )
    return user_info
