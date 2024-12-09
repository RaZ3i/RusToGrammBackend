from typing import Annotated

from fastapi import Depends, APIRouter
from jwt import ExpiredSignatureError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, FileResponse


from schemas.user_info import UserInfo, UserForSubList, SubCount, UserProfileInfo
from service.service import (
    get_user_profile_info,
    get_subscribes,
    subscribes_count,
    get_subscribers,
    subscribers_count,
    get_users_lists,
)
from utils.auth import (
    get_current_auth_user_from_cookie,
    get_current_auth_user_from_refresh,
)
from utils.pagination import Pagination, pagination_params

router = APIRouter(prefix="/profile", tags=["User_information"])


@router.get("/get_user_info_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_info_by_id(
    user_id: int,
):
    info = await get_user_profile_info(user_id=user_id)
    return info
    # return {"user_profile": info, "avatar": FileResponse(path=info.avatar_link).path}


@router.get("/get_avatar_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_avatar_by_id(
    user_id: int,
):
    info = await get_user_profile_info(user_id=user_id)
    avatar = FileResponse(path=info.avatar_link)
    return avatar


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
