from fastapi import HTTPException, status


class Errors:
    wrong_pass = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"success": False, "msg": "fail pass validation"},
    )
    wrong_login = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"success": False, "msg": "fail login validation"},
    )
    wrong_phone = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"success": False, "msg": "fail phone validation"},
    )
    inv_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "msg": "invalid token"},
    )
    inv_token_type = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "msg": "invalid token type"},
    )
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "msg": "wrong password or login"},
    )
    relog_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success": False, "msg": "login in your account"},
    )
    duplicate = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"success": False, "msg": "data already exist"},
    )
