from pydantic import BaseModel
from datetime import datetime


class UserProfileInfoIn(BaseModel):
    # user_id: int
    user_name: str | None = None
    description: str | None = None
    nickname: str | None = None
    # avatar_link: str


class PostData(BaseModel):
    user_id: int
    description: str
