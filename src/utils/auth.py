import datetime
import uuid
from datetime import timedelta
from typing import Annotated
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from fastapi import HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete, update
from starlette import status

from src.database import async_session_factory
from src.service.service import validate_password, get_user_data
from src.schemas.user_info import UserInfo, UserRefreshTokenData
from src.config import settings
from src.service.service import get_user_auth_info
from src.models.models import UserRefreshToken

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

inv_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
)
inv_token_type = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type"
)
unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password or login"
)
relog_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="login in your account"
)


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
    to_encode.update(exp=expire, iat=now, jti=uuid.uuid4().hex)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str,
    pulblic_key=settings.PUBLIC_KEY_PATH.read_text(),
    algoritm=settings.ALGORITHM,
):
    decoded = jwt.decode(token, pulblic_key, algorithms=[algoritm])
    return decoded


def decode_jwt_verify(
    token: str,
    pulblic_key=settings.PUBLIC_KEY_PATH.read_text(),
    algoritm=settings.ALGORITHM,
):
    decoded = jwt.decode(
        token,
        pulblic_key,
        algorithms=[algoritm],
        options={"verify_exp": False},
    )
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
    jwt_payload = {"sub": user["id"]}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


async def add_refresh_token_to_db(new_refresh_token: str):
    decode_data = decode_jwt(new_refresh_token)
    token_data = UserRefreshTokenData(
        user_id_refresh=decode_data["sub"],
        token_id=decode_data["jti"],
        refresh_token=new_refresh_token,
    )
    async with async_session_factory() as session:
        stmt1 = select(UserRefreshToken).where(
            UserRefreshToken.user_id_refresh == decode_data["sub"]
        )
        res = await session.execute(stmt1)
        if res:
            stmt2 = (
                update(UserRefreshToken)
                .where(UserRefreshToken.user_id_refresh == decode_data["sub"])
                .values(
                    token_id=token_data.token_id, refresh_token=token_data.refresh_token
                )
            )
            # stmt2 = delete(UserRefreshToken).where(
            #     UserRefreshToken.user_id_refresh == decode_data["sub"]
            # )
            await session.execute(stmt2)
            data = token_data.model_dump()
            # stmt3 = UserRefreshToken(**data)
            # session.add(stmt3)
            await session.flush()
            await session.commit()

        else:
            data = token_data.model_dump()
            stmt3 = UserRefreshToken(**data)
            session.add(stmt3)
            await session.flush()
            await session.commit()


async def get_refresh_token_from_db(user_id: int) -> dict:
    async with async_session_factory() as session:
        stmt = select(UserRefreshToken).where(
            UserRefreshToken.user_id_refresh == user_id
        )
        res = await session.execute(stmt)
        refresh_token = res.scalar().refresh_token
    return decode_jwt(refresh_token)


async def validate_auth_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        user = await get_user_auth_info(user_data.username)
        user_hash_pass = user["password"]
        if validate_password(user_data.password, user_hash_pass):
            return user
        else:
            raise unauthed_exc
    except:
        raise unauthed_exc


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise inv_token_type


async def get_current_auth_user_from_cookie(request: Request):
    try:
        payload = decode_jwt(request.cookies.get("users_access_token"))
        validate_token_type(payload, ACCESS_TOKEN_TYPE)
        return payload
    except ExpiredSignatureError:
        return ExpiredSignatureError
    except DecodeError:
        raise relog_exc
    #     payload1 = decode_jwt_verify(request.cookies.get("users_access_token"))
    #     current_user = await get_current_auth_user_from_refresh(
    #         access_token_payload=payload1
    #     )
    #     return current_user
    # except:
    #     raise inv_token


async def get_current_auth_user_from_refresh(request: Request):
    try:
        access_token_exp = decode_jwt_verify(request.cookies.get("users_access_token"))
        refresh_token_payload = await get_refresh_token_from_db(
            user_id=access_token_exp["id"]
        )
        validate_token_type(refresh_token_payload, REFRESH_TOKEN_TYPE)
        user_login: str | None = access_token_exp.get("login")
        user = await get_user_data(user_login=user_login)
        user_info = {"login": user.login, "id": user.id}
        access_token = create_access_token(user=user_info)
        # refresh_token = create_refresh_token(user=user_info)
        # print(f"refresh_token: {refresh_token},\naccess_token: {access_token}")
        # await add_refresh_token_to_db(refresh_token)
        return {"user_info": user_info, "access_token": access_token}
    except DecodeError:
        raise inv_token
