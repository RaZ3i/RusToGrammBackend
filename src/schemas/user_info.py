from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    login: str
    phone: str


class UserRefreshTokenData(BaseModel):
    user_id_refresh: int
    token_id: str
    refresh_token: str
