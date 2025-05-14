from fastapi import HTTPException, status


class Errors:
    wrong_data = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"success": False}
    )

    inv_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "code": 94, "msg": "Ошибка проверки данных"},
    )
    inv_token_type = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "msg": "Не удалось идентифицировать токен"},
    )
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "msg": "Неверный логин или пароль"},
    )
    relog_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "code": 93, "msg": "Требуется повторная авторизация"},
    )
    duplicate = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"success": False,
                "errors": [
                    {"code": 95, "msg": "Такой пользователь уже существует"}
                ]},
    )
