from fastapi import Depends, APIRouter
from jwt import ExpiredSignatureError
from starlette.requests import Request
from starlette.responses import Response

from schemas.user_info import UserInfo
from utils.auth import (
    get_current_auth_user_from_cookie,
    get_current_auth_user_from_refresh,
)

router = APIRouter(prefix="/profile", tags=["Profile_operation"])


@router.post("/post")
async def create_post(
    response: Response,
    request: Request,
    post_data: str,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        response.delete_cookie(key="users_access_token", domain="localhost")
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        return {"post_data": post_data, "current_user": current_user}
    else:
        return {"post_data": post_data, "current_user": current_user}
