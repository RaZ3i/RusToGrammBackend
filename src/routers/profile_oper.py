import os
import uuid
from pathlib import Path
import re
from fastapi import Depends, APIRouter, UploadFile, Request
import shutil
from starlette import status

from src.schemas.user_info_in import UserProfileInfoIn, CommentData, LikeData
from src.service.service import (
    add_avatar_link,
    subscribe,
    add_post,
    update_profile,
    create_comment_post,
    like_post,
    delete_user_avatar_link,
)
from src.schemas.user_info import UserInfo, SuccessResponse, AvatarLinkResponse
from src.utils.auth import (
    get_current_auth_user_from_cookie,
)
from src.utils.files import add_new_file, delete_user_avatar, add_avatar


router = APIRouter(prefix="/profile", tags=["Profile_operation"])


# дописать проверку на тип загружаемого файла
@router.post(
    "/upload_avatar/", status_code=status.HTTP_200_OK, response_model=AvatarLinkResponse
)
async def upload_avatar(
    avatar: UploadFile,
    request: Request,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    try:
        res_1 = await add_avatar(
            avatar=avatar, user_id=current_user["id"], request=request
        )
        await add_avatar_link(
            user_id=current_user["id"], avatar_link=res_1["avatar_link"]
        )
        return res_1
    except:
        return {"success": False, "avatar_link": None}


@router.patch("/delete_avatar/", status_code=status.HTTP_200_OK)
async def delete_avatar(
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    res = await delete_user_avatar_link(user_id=current_user["id"])
    return res


@router.post("/subscribe_at/{sub_id}", status_code=status.HTTP_200_OK)
async def subscribe_at(
    sub_id: int,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    res = await subscribe(user_id=current_user["id"], subscribe_id=sub_id)
    return res


@router.post("/create_post/", status_code=status.HTTP_201_CREATED)
async def post(
    description: str,
    files: list[UploadFile],
    request: Request,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    post_id = str(uuid.uuid4())
    arr_link = add_new_file(files=files, post_id=post_id, request=request)
    if arr_link["success"] is True:
        res = await add_post(
            post_id=post_id,
            user_id=current_user["id"],
            description=description,
            files=files,
            file_link=arr_link["links"],
        )
        return res
    else:
        return arr_link


@router.patch(
    "/modify_my_info/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse,
)
async def modify_my_info(
    new_data: UserProfileInfoIn,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    new_data = new_data.model_dump(exclude_none=True, exclude_unset=True)
    return await update_profile(user_id=current_user["id"], profile_data=new_data)


@router.post("/comment_post/")
async def create_comment(
    comment_data: CommentData,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    return await create_comment_post(
        post_id=comment_data.post_id,
        user_id=current_user["id"],
        comment_text=comment_data.text,
    )


@router.post("/post_like/")
async def post_like(
    post_id: int,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    return await like_post(
        post_id=post_id,
        user_id=current_user["id"],
    )
