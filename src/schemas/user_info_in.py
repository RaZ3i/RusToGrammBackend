from pydantic import BaseModel
from datetime import datetime


class UserProfileInfoIn(BaseModel):
    # user_id: int
    user_name: str | None = None
    description: str | None = None
    nickname: str | None = None
    # avatar_link: str


class CommentData(BaseModel):
    post_id: int
    text: str


class LikeData(BaseModel):
    post_id: int
    user_id: int
