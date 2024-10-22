from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    login: str
    phone: str
