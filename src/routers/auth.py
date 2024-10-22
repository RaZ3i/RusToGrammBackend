from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer

from src.schemas.user_info import UserInfo
from src.schemas.authout import UserRegisterOut, UserAuthLoginOut
from src.schemas.authin import UserRegisterIn, UserAuthLoginIn
from src.service.service import (
    create_user,
)
from src.utils.auth import (
    validate_auth_user,
    get_current_auth_user,
    get_current_auth_user_for_refresh,
)
from src.utils.auth import create_access_token, create_refresh_token

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])


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
async def login(user_data: UserAuthLoginIn = Depends(validate_auth_user)):
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post(
    "/refresh/", response_model=UserAuthLoginOut, response_model_exclude_none=True
)
async def auth_refresh_jwt(user: UserInfo = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    return {
        "success": True,
        "access_token": access_token,
    }


@router.get("/users/me")
async def get_my_info(user: UserInfo = Depends(get_current_auth_user)):
    return {"id": user.id, "login": user.login, "phone": user.phone}
