import bcrypt
from sqlalchemy import select
from src.database import async_session_factory
from src.schemas.authin import UserRegisterIn
from src.models.models import User, UserProtect


async def get_user_id(user_login: str):
    async with async_session_factory() as session:
        stmt1 = select(User).where(User.login == user_login)
        res = await session.execute(stmt1)
        user_id = res.scalar().id
        return user_id


async def get_user_data(user_login: str):
    async with async_session_factory() as session:
        stmt1 = select(User).where(User.login == user_login)
        res = await session.execute(stmt1)
        user_data = res.scalar()
        return user_data


async def get_user_auth_info(login: str):
    async with async_session_factory() as session:
        stmt1 = select(User).where(User.login == login)
        res1 = await session.execute(stmt1)
        user_auth_info1 = res1.scalar()
        stmt2 = select(UserProtect).where(UserProtect.user_id == user_auth_info1.id)
        res2 = await session.execute(stmt2)
        user_auth_info2 = res2.scalar().long_hashed_password
        return {
            "id": user_auth_info1.id,
            "login": user_auth_info1.login,
            "password": user_auth_info2,
        }


async def create_user(new_user: UserRegisterIn):
    async with async_session_factory() as session:
        data1 = new_user.model_dump(include={"login", "phone", "email"})
        stmt1 = User(**data1)
        session.add(stmt1)
        await session.flush()
        await session.commit()
        user_id = await get_user_id(data1["login"])
        data2 = new_user.model_dump(
            include={"long_hashed_password", "short_hashed_password"}
        )
        data2["user_id"] = user_id
        data2["long_hashed_password"] = hash_password(data2["long_hashed_password"])
        stmt2 = UserProtect(**data2)
        session.add(stmt2)
        await session.flush()
        await session.commit()
        return {"success": True}


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_password)
