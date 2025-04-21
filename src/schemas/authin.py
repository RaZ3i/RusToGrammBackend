from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    field_validator,
    model_validator,
)
from email_validator import validate_email, EmailNotValidError
from typing import Annotated, Any
import re
from src.errors import Errors


class UserRegisterIn(BaseModel):
    # model_config = ConfigDict(regex_engine="python-re")
    login: str
    phone: str
    email: str
    # email: EmailStr
    long_hashed_password: str
    short_hashed_password: str

    @model_validator(mode="before")
    @classmethod
    def check_inputs(cls, data: dict):
        output_data = []
        if isinstance(data, dict):
            if not re.match(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{4,15}$",
                data["login"],
            ):
                output_data.append(
                    {
                        "code": 99,
                        "msg": "Логин должен содержать:\n- От 4 до 15 символов;\n- Латинские большие и маленькие буквы;\n- Цифры.",
                    }
                )
            if not re.match(
                r"^(8|\+7)\d{10}$",
                data["phone"],
            ):
                output_data.append(
                    {
                        "code": 96,
                        "msg": "Ошибка в формате номера телефона.\nПример: +7-xxx-xxx-xx-xx/8-xxx-xxx-xx-xx.",
                    }
                )
            if not re.match(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$",
                data["long_hashed_password"],
            ):
                output_data.append(
                    {
                        "code": 98,
                        "msg": "Пароль должен содержать:\n- Минимум 10 символов;\n- Латинские большие и маленькие буквы;\n- цифры;\n- спецсимволы.",
                    }
                )
            try:
                validate_email(data["email"])
            except EmailNotValidError:
                output_data.append(
                    {
                        "code": 97,
                        "msg": "Email не прошел проверку.\nПример e-mail: example@mail.ru",
                    }
                )
            finally:
                if len(output_data) == 0:
                    return data
                else:
                    err = Errors.wrong_data
                    err.detail.update({"errors": output_data})
                    raise err

    # @field_validator("login")
    # @classmethod
    # def login_match(cls, value: str):
    #     if not re.match(
    #         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{4,15}$",
    #         value,
    #     ):
    #         raise Errors.wrong_login
    #     return value
    #
    # @field_validator("phone")
    # @classmethod
    # def phone_match(cls, value: str):
    #     if not re.match(
    #         r"^(8|\+7)\d{10}$",
    #         value,
    #     ):
    #         raise Errors.wrong_phone
    #     return value
    #
    # @field_validator("long_hashed_password")
    # @classmethod
    # def passwords_match(cls, value: str):
    #     if not re.match(
    #         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$",
    #         value,
    #     ):
    #         raise Errors.wrong_pass
    #     return value

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
