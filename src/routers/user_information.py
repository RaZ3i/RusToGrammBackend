from typing import Annotated, List

from fastapi import Depends, APIRouter
from starlette import status
from starlette.responses import FileResponse

from src.errors import Errors
from src.schemas.user_info import UserInfo, UserForSubList, SubCount, UserProfileInfo
from src.service.service import (
    get_user_profile_info,
    get_subscribes,
    subscribes_count,
    get_subscribers,
    subscribers_count,
    get_users_lists,
    get_users_posts,
    get_comments_post,
)
from src.utils.auth import (
    get_current_auth_user_from_cookie,
)
from src.utils.pagination import Pagination, pagination_params

router = APIRouter(prefix="/profile", tags=["User_information"])


@router.get(
    "/get_user_info_by_id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileInfo,
)
async def get_user_info_by_id(user_id: int):
    try:
        info = await get_user_profile_info(user_id=user_id)
        return info
    except:
        return user_id
    # return {"user_profile": info, "avatar": FileResponse(path=info.avatar_link).path}


@router.get("/get_avatar_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_avatar_by_id(
    user_id: int,
):
    info = await get_user_profile_info(user_id=user_id)
    if info.avatar_link is None:
        raise Errors.file_exc
    else:
        # avatar = FileResponse(path=str(info.avatar_link))
        return {"success": True, "avatar_link": info.avatar_link}


# Убрать current_user позже и сделать чтобы функция просто принимала user_id
@router.get(
    "/subscribes_list/",
    response_model=list[UserForSubList],
    status_code=status.HTTP_200_OK,
)
async def get_subscribes_list(
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    users_list = await get_subscribes(user_id=current_user["id"])
    return users_list


@router.get(
    "/subscribes_count/",
    response_model=SubCount,
    status_code=status.HTTP_200_OK,
)
async def get_subscribes_count(
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    try:
        count = await subscribes_count(user_id=current_user["id"])
        return count
    except:
        raise Errors.relog_exc


@router.get(
    "/subscribers_list/",
    response_model=list[UserForSubList],
    status_code=status.HTTP_200_OK,
)
async def get_subscribers_list(
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    users_list = await get_subscribers(user_id=current_user["id"])
    return users_list


@router.get(
    "/subscribers_count/",
    response_model=SubCount,
    status_code=status.HTTP_200_OK,
)
async def get_subscribers_count(
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    try:
        count = await subscribers_count(user_id=current_user["id"])
        return count
    except:
        raise Errors.relog_exc


@router.get(
    "/my_info/",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileInfo,
)
async def get_my_info(
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    try:
        info = await get_user_profile_info(user_id=current_user["id"])
        return info
    except:
        raise Errors.relog_exc


@router.get(
    "/users_list/", status_code=status.HTTP_200_OK, response_model=list[UserProfileInfo]
)
async def get_users(
    pagination: Annotated[Pagination, Depends(pagination_params)],
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    users_list = await get_users_lists(
        user_id=current_user["id"], perpage=pagination.perPage, page=pagination.page
    )
    return users_list


@router.get("/user_posts/", status_code=status.HTTP_200_OK)
async def get_posts(user_id: int, posts_limit: int, page: int):
    res = await get_users_posts(user_id=user_id, posts_limit=posts_limit, page=page)
    return res


@router.get("/comments_post/", status_code=status.HTTP_200_OK)
async def get_comments(post_id: int):
    res = await get_comments_post(post_id=post_id)
    return res
