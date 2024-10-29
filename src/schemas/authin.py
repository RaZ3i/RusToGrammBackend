from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from fastapi import HTTPException, status
import re

wrong_pass = {
    "error": HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="fail pass validation"
    ),
    "success": False,
}


class UserRegisterIn(BaseModel):
    # model_config = ConfigDict(regex_engine="python-re")
    login: str
    phone: str
    email: EmailStr
    long_hashed_password: str
    # long_hashed_password: str = Field(
    #     pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$",
    # )
    short_hashed_password: str

    @field_validator("long_hashed_password")
    @classmethod
    def passwords_match(cls, value: str):
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$",
            value,
        ):
            raise wrong_pass
        return value


class UserAuthLoginIn(BaseModel):
    login: str
    long_password: str


class UserAuthPhoneIn(BaseModel):
    login: str
    long_password: str
