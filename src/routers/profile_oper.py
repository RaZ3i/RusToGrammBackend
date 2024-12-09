import uuid
from pathlib import Path
import re
from fastapi import Depends, APIRouter, UploadFile
import shutil
from jwt import ExpiredSignatureError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from schemas.user_info_in import UserProfileInfoIn
from service.service import (
    add_avatar_link,
    subscribe,
    add_post,
    update_profile,
)
from src.schemas.user_info import (
    UserInfo,
    SuccessResponse,
)
from utils.auth import (
    get_current_auth_user_from_cookie,
    get_current_auth_user_from_refresh,
)
from utils.files import add_new_file

router = APIRouter(prefix="/profile", tags=["Profile_operation"])


# дописать проверку на тип загружаемого файла
@router.post("/upload_avatar/", status_code=status.HTTP_200_OK)
async def upload_avatar(
    response: Response,
    request: Request,
    avatar: UploadFile,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
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


@router.post("/subscribe_at/{sub_id}", status_code=status.HTTP_200_OK)
async def subscribe_at(
    sub_id: int,
    response: Response,
    request: Request,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        res = await subscribe(
            user_id=current_user["user_info"]["id"], subscribe_id=sub_id
        )
        return res
    else:
        res = await subscribe(user_id=current_user["id"], subscribe_id=sub_id)
        return res


@router.post("/create_post/", status_code=status.HTTP_201_CREATED)
async def post(
    description: str,
    files: list[UploadFile],
    response: Response,
    request: Request,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        post_id = str(uuid.uuid4())
        arr_link = add_new_file(files=files, post_id=post_id)
        # print(arr_link)
        if arr_link["success"]:
            res = await add_post(
                post_id=post_id,
                user_id=current_user["user_info"]["id"],
                description=description,
                files=files,
                file_link=arr_link["links"],
            )
            return res
        else:
            return arr_link
    else:
        post_id = str(uuid.uuid4())
        arr_link = add_new_file(files=files, post_id=post_id)
        res = await add_post(
            post_id=post_id,
            user_id=current_user["id"],
            description=description,
            files=files,
            file_link=arr_link,
        )
        return res


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
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        new_data = new_data.model_dump(exclude_none=True, exclude_unset=True)
        return await update_profile(
            user_id=current_user["user_info"]["id"], profile_data=new_data
        )
    else:
        new_data = new_data.model_dump(exclude_none=True, exclude_unset=True)
        return await update_profile(user_id=current_user["id"], profile_data=new_data)


# @router.post("/post/", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
# async def create_post(
#     response: Response,
#     request: Request,
#     post_data: str,
#     current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
# ):
#     if current_user == ExpiredSignatureError:
#         current_user = await get_current_auth_user_from_refresh(request=request)
#         response.set_cookie(
#             key="users_access_token",
#             value=current_user["access_token"],
#             httponly=True,
#         )
#         return {"success": True, "post_data": post_data, "current_user": current_user}
#     else:
#         return {"success": True, "post_data": post_data, "current_user": current_user}
