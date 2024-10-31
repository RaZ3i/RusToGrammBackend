from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Annotated
import re
from errors import Errors


class UserRegisterIn(BaseModel):
    # model_config = ConfigDict(regex_engine="python-re")
    login: str
    phone: str
    email: EmailStr
    long_hashed_password: str
    short_hashed_password: str

    @field_validator("login")
    @classmethod
    def login_match(cls, value: str):
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{4,15}$",
            value,
        ):
            raise Errors.wrong_login
        return value

    @field_validator("phone")
    @classmethod
    def phone_match(cls, value: str):
        if not re.match(
            r"^(8|\+7)\d{10}$",
            value,
        ):
            raise Errors.wrong_phone
        return value

    @field_validator("long_hashed_password")
    @classmethod
    def passwords_match(cls, value: str):
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$",
            value,
        ):
            raise Errors.wrong_pass
        return value

    # long_hashed_password: Annotated[
    #     str,
    #     Field(
    #         ...,
    #         pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{4,}$",
    #     ),
    # ]


class UserAuthLoginIn(BaseModel):
    login: str
    long_password: str


class UserAuthPhoneIn(BaseModel):
    login: str
    long_password: str
