from fastapi import APIRouter, status, Depends, Response

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
)

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
    response: Response, new_user: UserRegisterIn,
):
    user = await create_user(new_user)
    if user['success']:
        access_token = create_access_token(user['user_info'])
        refresh_token = create_refresh_token(user['user_info'])
        await add_refresh_token_to_db(refresh_token)

        response.set_cookie(
            key="users_access_token",
            value=access_token,
            # domain="127.0.0.1",
            httponly=True,
        )
        return {
            "success": True
        }
    return user


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(
    response: Response, user_data: UserAuthLoginIn = Depends(validate_auth_user)
):
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    await add_refresh_token_to_db(refresh_token)
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        # domain="127.0.0.1",
        httponly=True,
    )
    return {
        "success": True,
        # "access_token": access_token,
        # "refresh_token": refresh_token,
    }


# @router.get("/users/me_from cookie")
# async def get_my_info(user: UserInfo = Depends(get_current_auth_user_from_cookie)):
#     return user


@router.post("/logout/")
async def logout(
    response: Response,
):
    response.delete_cookie(key="users_access_token", domain="127.0.0.1")
    return {"success": True}


# @router.get("/refresh")
# async def get_my_info(user: UserInfo = Depends(get_current_auth_user_from_cookie)):
#     token = await get_refresh_token_from_db(user["id"])
#     return token
