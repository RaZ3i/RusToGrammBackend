from pathlib import Path
import re
from fastapi import Depends, APIRouter, status, UploadFile
import shutil
from jwt import ExpiredSignatureError
from starlette.requests import Request
from starlette.responses import Response, FileResponse
from service.service import get_user_profile_info, update_profile, add_avatar_link
from src.schemas.user_info import UserInfo, UserProfileInfo, SuccessResponse
from src.schemas.user_info_in import UserProfileInfoIn
from src.utils.auth import (
    get_current_auth_user_from_cookie,
    get_current_auth_user_from_refresh,
)

router = APIRouter(prefix="/profile", tags=["Profile_operation"])


@router.get(
    "/my_info/",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileInfo,
)
async def get_my_info(
    response: Response,
    request: Request,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        # response.delete_cookie(key="users_access_token", domain="localhost")
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        info = await get_user_profile_info(user_id=current_user["user_info"]["id"])
        return info
    else:
        info = await get_user_profile_info(user_id=current_user["id"])
        return info


@router.patch(
    "/modify_my_info/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse,
)
async def modify_my_info(
    response: Response,
    request: Request,
    new_data: UserProfileInfoIn,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        # response.delete_cookie(key="users_access_token", domain="localhost")
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        new_data = new_data.model_dump(exclude_none=True)
        return await update_profile(
            user_id=current_user["user_info"]["id"], profile_data=new_data
        )
    else:
        new_data = new_data.model_dump(exclude_none=True)
        return await update_profile(user_id=current_user["id"], profile_data=new_data)


@router.post("/post/", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
async def create_post(
    response: Response,
    request: Request,
    post_data: str,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        # response.delete_cookie(key="users_access_token", domain="localhost")
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        return {"success": True, "post_data": post_data, "current_user": current_user}
    else:
        return {"success": True, "post_data": post_data, "current_user": current_user}


@router.post("/upload_avatar/", status_code=status.HTTP_200_OK)
async def upload_avatar(
    response: Response,
    request: Request,
    avatar: UploadFile,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        # response.delete_cookie(key="users_access_token", domain="localhost")
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )

        avatars_dir = (
            Path(__file__).parent.parent.parent
            / f"Files/Avatars/{avatar.filename.replace(avatar.filename,
                                                           f"user_{current_user["user_info"]["id"]}_avatar.{(re.search(r"(jpeg)|(png)", avatar.content_type)).group()}")}"
        )

        with open(avatars_dir, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        await add_avatar_link(
            user_id=current_user["user_info"]["id"], avatar_link=str(avatars_dir)
        )
        return {"success": True, "avatar_link": avatars_dir}
    else:
        avatars_dir = (
            Path(__file__).parent.parent.parent
            / f"Files/Avatars/{avatar.filename.replace(avatar.filename,
                                                           f"user_{current_user["id"]}_avatar.{(re.search(r"(jpeg)|(png)", avatar.content_type)).group()}")}"
        )

        with open(avatars_dir, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        await add_avatar_link(user_id=current_user["id"], avatar_link=str(avatars_dir))
        return {"success": True, "avatar_link": avatars_dir}


@router.get("/get_user_info_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_info_by_id(
    user_id: int,
):
    info = await get_user_profile_info(user_id=user_id)
    return {"user_profile": info, "avatar": FileResponse(path=info.avatar_link)}


@router.get("/get_avatar_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_avatar_by_id(
    user_id: int,
):
    info = await get_user_profile_info(user_id=user_id)
    return FileResponse(path=info.avatar_link)
