import datetime

from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    login: str
    phone: str | None = None


class UserProfileInfo(BaseModel):
    user_id: int
    user_name: str | None = None
    description: str | None = None
    nickname: str
    avatar_link: str | None = None
    followers_count: int | str
    subscribes_count: int | str
    private_account: bool | None = None


class SubCount(BaseModel):
    count: int
    success: bool


class UserForSubList(BaseModel):
    user_id: int
    nickname: str
    avatar_link: str | None = None


class UserRefreshTokenData(BaseModel):
    user_id_refresh: int
    token_id: str
    refresh_token: str


class SuccessResponse(BaseModel):
    success: bool
    changed: bool


class AvatarLinkResponse(BaseModel):
    success: bool
    avatar_link: str


class UserPostsResponse(BaseModel):
    id: int
    user_id: int
    desscription: str
    posted_at: datetime.datetime
    photo_links: list[str]
    likes_count: int
    comments_count: int


class PostCommentsResponse(BaseModel):
    post_id: int
    user_id: int
    comment_text: str
    nickname: str
    avatar_link: str
    created_at: datetime.datetime
