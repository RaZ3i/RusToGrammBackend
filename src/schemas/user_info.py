from pydantic import BaseModel
from typing_extensions import TypedDict


class UserInfo(BaseModel):
    id: int
    login: str
    phone: str | None = None


class UserProfileInfo(BaseModel):
    user_id: int
    user_name: str | None = None
    description: str | None = None
    nickname: str
    private_account: bool | None = None
    avatar_link: str | None = None


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
