from pydantic import BaseModel
from datetime import datetime


class UserRegisterIn(BaseModel):
    login: str
    phone: str
    long_hashed_password: str
    short_hashed_password: str


class UserAuthLoginIn(BaseModel):
    login: str
    long_password: str


class UserAuthPhoneIn(BaseModel):
    login: str
    long_password: str
