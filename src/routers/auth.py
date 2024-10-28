import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends, Response, Request
from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError

from src.schemas.user_info import UserInfo
from src.schemas.authout import UserRegisterOut, UserAuthLoginOut
from src.schemas.authin import UserRegisterIn, UserAuthLoginIn
from src.service.service import (
    create_user,
)
from src.utils.auth import (
    validate_auth_user,
    get_current_auth_user_from_cookie,
    add_refresh_token_to_db,
    get_refresh_token_from_db,
    get_current_auth_user_from_refresh,
)
from src.config import settings

# from trash import get_current_auth_user, get_current_auth_user_for_refresh
from src.utils.auth import create_access_token, create_refresh_token

# http_bearer = HTTPBearer(auto_error=False)
# router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterOut,
)
async def registration(
    new_user: UserRegisterIn,
):
    result = await create_user(new_user)
    return result


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=UserAuthLoginOut)
async def login(
    response: Response, user_data: UserAuthLoginIn = Depends(validate_auth_user)
):
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    await add_refresh_token_to_db(refresh_token)
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
    )
    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


# @router.post(
#     "/refresh/", response_model=UserAuthLoginOut, response_model_exclude_none=True
# )
# # async def auth_refresh_jwt(user: UserInfo = Depends(get_current_auth_user_for_refresh)):
# #     access_token = create_access_token(user)
# #     return {
# #         "success": True,
# #         "access_token": access_token,
# #     }
# #
# #


@router.get("/users/me_from cookie")
async def get_my_info(user: UserInfo = Depends(get_current_auth_user_from_cookie)):
    return user
    # return {"id": user.id, "login": user.login, "phone": user.phone}


@router.get("/refresh")
async def get_my_info(user: UserInfo = Depends(get_current_auth_user_from_cookie)):
    token = await get_refresh_token_from_db(user["id"])
    return token
    # return {"id": user.id, "login": user.login, "phone": user.phone}


@router.post("/login/post")
async def create_post(
    response: Response,
    request: Request,
    post_data: str,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        print(current_user)
        response.delete_cookie(key="users_access_token", domain="localhost")
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        return {"post_data": post_data, "current_user": current_user}
    else:
        return {"post_data": post_data, "current_user": current_user}


@router.post("/login/logout")
async def logout(
    response: Response,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    response.delete_cookie(key="users_access_token", domain="localhost")
    return {"success": True}
