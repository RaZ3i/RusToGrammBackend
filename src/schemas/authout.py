from pydantic import BaseModel


class UserRegisterOut(BaseModel):
    success: bool


class UserAuthLoginOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    success: bool


class UserAuthPhoneOut(BaseModel):
    success: bool
