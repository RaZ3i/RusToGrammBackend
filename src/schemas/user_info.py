from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    login: str
    phone: str


class UserProfileInfo(BaseModel):
    user_id: int
    user_name: str | None = None
    description: str | None = None
    nickname: str
    private_account: bool
    avatar_link: str | None = None


class SuccessResponse(BaseModel):
    success: bool
    changed: bool


class UserRefreshTokenData(BaseModel):
    user_id_refresh: int
    token_id: str
    refresh_token: str
