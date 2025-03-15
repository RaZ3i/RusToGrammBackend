from fastapi import HTTPException, status


class Errors:
    wrong_data = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"success": False}
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
