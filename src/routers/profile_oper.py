from pathlib import Path
import re
from typing import Annotated, List
import os
from fastapi import Depends, APIRouter, status, UploadFile
import shutil
from jwt import ExpiredSignatureError
from starlette.requests import Request
from starlette.responses import Response, FileResponse
from service.service import (
    get_user_profile_info,
    update_profile,
    add_avatar_link,
    get_users_lists,
    subscribe,
    get_subscribes,
    get_subscribers,
    subscribers_count,
    subscribes_count,
)
from src.schemas.user_info import (
    UserInfo,
    UserProfileInfo,
    UserForSubList,
    SuccessResponse,
    SubCount,
)
from src.schemas.user_info_in import UserProfileInfoIn, PostData
from src.utils.auth import (
    get_current_auth_user_from_cookie,
    get_current_auth_user_from_refresh,
)
from utils.pagination import Pagination, pagination_params

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


@router.post("/post/", status_code=status.HTTP_200_OK, response_model=SuccessResponse)
async def create_post(
    response: Response,
    request: Request,
    post_data: str,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
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


@router.get(
    "/users_list/", status_code=status.HTTP_200_OK, response_model=list[UserProfileInfo]
)
async def get_users(
    pagination: Annotated[Pagination, Depends(pagination_params)],
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
        users_list = await get_users_lists(
            user_id=current_user["user_info"]["id"],
            perpage=pagination.perPage,
            page=pagination.page,
        )
        return users_list
    else:
        users_list = await get_users_lists(
            user_id=current_user["id"], perpage=pagination.perPage, page=pagination.page
        )
        return users_list


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


# Убрать current_user позже и сделать чтобы функция просто принимала user_id
@router.get(
    "/subscribes_list/",
    response_model=list[UserForSubList],
    status_code=status.HTTP_200_OK,
)
async def get_subscribes_list(
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
        users_list = await get_subscribes(user_id=current_user["user_info"]["id"])
        return users_list
    else:
        users_list = await get_subscribes(user_id=current_user["id"])
        return users_list


@router.get(
    "/subscribes_count/",
    response_model=SubCount,
    status_code=status.HTTP_200_OK,
)
async def get_subscribes_count(
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
        count = await subscribes_count(user_id=current_user["user_info"]["id"])
        return count
    else:
        count = await subscribes_count(user_id=current_user["id"])
        return count


@router.get(
    "/subscribers_list/",
    response_model=list[UserForSubList],
    status_code=status.HTTP_200_OK,
)
async def get_subscribers_list(
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
        users_list = await get_subscribers(user_id=current_user["user_info"]["id"])
        return users_list
    else:
        users_list = await get_subscribers(user_id=current_user["id"])
        return users_list


@router.get(
    "/subscribers_count/",
    response_model=SubCount,
    status_code=status.HTTP_200_OK,
)
async def get_subscribers_count(
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
        count = await subscribers_count(user_id=current_user["user_info"]["id"])
        return count
    else:
        count = await subscribers_count(user_id=current_user["id"])
        return count


@router.post("/create_post/", status_code=status.HTTP_201_CREATED)
async def post(
    # post_data: PostData,
    files: list[UploadFile] | UploadFile,
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
        post_dir = f"../Files/Photos/{current_user["user_info"]["id"]}"
        os.makedirs(post_dir)
        for file in files:
            print(file.filename)
            file.filename = f"file_{current_user["user_info"]["id"]}_{file.size}.{(re.search(r"(jpeg)|(png)", file.content_type)).group()}"
            with open(post_dir + "/" + file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        return True

    else:
        post_dir = f"../Files/Photos/{current_user["id"]}"
        os.makedirs(post_dir)
        for file in files:
            print(file.filename)
            file.filename = f"file_{current_user["id"]}_{file.size}.{(re.search(r"(jpeg)|(png)", file.content_type)).group()}"
            with open(post_dir + "/" + file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)


#     photos_dir = (
#         Path(__file__).parent.parent.parent
#         / f"Files/Photos/{photos.filename.replace(photos.filename,
#                                                       f"user_{current_user["user_info"]["id"]}_avatar.{(re.search(r"(jpeg)|(png)", photos.content_type)).group()}")}"
#     )
#
#     with open(photos_dir, "wb") as buffer:
#         shutil.copyfileobj(photos.file, buffer)
#     return {"success": True, "photos_link": photos_dir}
# else:
#     photos_dir = (
#         Path(__file__).parent.parent.parent
#         / f"Files/Photos/{photos.filename.replace(photos.filename,
#                                                       f"user_{current_user["id"]}_avatar.{(re.search(r"(jpeg)|(png)", photos.content_type)).group()}")}"
#     )
#
#     with open(photos_dir, "wb") as buffer:
#         shutil.copyfileobj(photos.file, buffer)
#     await add_avatar_link(user_id=current_user["id"], avatar_link=str(photos_dir))
#     return {"success": True, "photos_link": photos_dir}
