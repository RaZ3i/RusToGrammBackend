import datetime
from pathlib import Path

import bcrypt
import uuid

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, or_, and_, asc, desc
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.functions import count, func

from src.database import async_session_factory
from src.schemas.authin import UserRegisterIn
from src.schemas.user_info import UserInfo
from src.models.models import (
    User,
    UserProtect,
    UserProfile,
    UserSubscribes,
    UserSubscribers,
    Posts,
    Photos,
    Comments,
    Likes,
    Messages,
)
from src.errors import Errors
from src.utils.files import delete_user_avatar


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
        try:
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
            stmt3 = UserProfile(
                user_id=user_id,
                user_profile_id=user_id,
                nickname="user" + str(uuid.uuid4().time),
            )
            session.add_all([stmt2, stmt3])
            await session.flush()
            await session.commit()
            user_data = {
                "id": user_id,
                "login": data1["login"],
                "phone": data1["phone"],
            }
            return {"success": True, "user_info": user_data}
        except IntegrityError:
            raise Errors.duplicate


async def update_profile(user_id: int, profile_data: dict):
    async with async_session_factory() as session:
        # data = profile_data.model_dump(exclude_none=True, exclude_unset=True)
        # print(data)
        # new_data = UserProfile(**data)
        stmt = (
            update(UserProfile)
            .where(UserProfile.user_id == user_id)
            .values(profile_data)
        )
        await session.execute(stmt)
        await session.flush()
        await session.commit()
        return {"success": True, "changed": True}


async def add_avatar_link(user_id: int, avatar_link: str):
    async with async_session_factory() as session:
        stmt = (
            update(UserProfile)
            .where(UserProfile.user_id == user_id)
            .values(avatar_link=avatar_link)
        )
        await session.execute(stmt)
        await session.flush()
        await session.commit()
        return {"success": True, "changed": True}


async def delete_user_avatar_link(user_id: int):
    async with async_session_factory() as session:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(avatar_link=None)
        )
        await session.execute(stmt)
        await session.commit()
    await delete_user_avatar(user_id=user_id)
    return {"success": True}


async def get_users_lists(user_id: int, perpage: int, page: int):
    async with async_session_factory() as session:
        stmt = (
            select(
                UserProfile.user_id,
                UserProfile.user_name,
                UserProfile.nickname,
                UserProfile.description,
                UserProfile.avatar_link,
            )
            .where(UserProfile.user_id != user_id)
            .limit(perpage)
            .offset(page - 1 if page == 1 else (page - 1) * perpage)
        )
        res = await session.execute(stmt)
        user_list = res.mappings().fetchmany()
        # count = await session.execute()
        return user_list


async def get_user_profile_info(user_id: int):
    async with async_session_factory() as session:
        followers_count_subq = (
            select(func.count(UserSubscribers.subscribers_id))
            .where(UserSubscribers.user_id == user_id)
            .scalar_subquery()
        )
        subscribes_count_subq = (
            select(func.count(UserSubscribes.subscribes_id))
            .where(UserSubscribes.user_id == user_id)
            .scalar_subquery()
        )
        stmt = select(
            UserProfile.user_id,
            UserProfile.nickname,
            UserProfile.user_name,
            UserProfile.description,
            UserProfile.avatar_link,
            followers_count_subq.label("followers_count"),
            subscribes_count_subq.label("subscribes_count"),
            UserProfile.private_account,
        ).where(UserProfile.user_id == user_id)
        res = await session.execute(stmt)
        profile_data = res.mappings().fetchmany()
        return profile_data[0]


async def subscribe(user_id: int, subscribe_id: int):
    async with async_session_factory() as session:
        data = {"user_id": user_id, "subscribes_id": subscribe_id}
        stmt = UserSubscribes(**data)
        session.add(stmt)
        await add_to_subscribers_table(user_id=subscribe_id, subscriber_id=user_id)
        await session.flush()
        await session.commit()
    return {"success": True}


async def get_subscribes(user_id: int):
    async with async_session_factory() as session:
        stmt = (
            select(UserProfile.user_id, UserProfile.nickname, UserProfile.avatar_link)
            .join_from(
                UserSubscribes,
                UserProfile,
                UserSubscribes.subscribes_id == UserProfile.user_id,
            )
            .where(UserSubscribes.user_id == user_id)
        )
        data = await session.execute(stmt)
        res = data.mappings().fetchmany()
    return res


async def subscribes_count(user_id: int):
    async with async_session_factory() as session:
        stmt = (
            select(UserProfile.user_id)
            .join_from(
                UserSubscribes,
                UserProfile,
                UserSubscribes.subscribes_id == UserProfile.user_id,
            )
            .where(UserSubscribes.user_id == user_id)
        )
        data = await session.execute(stmt)
        res = data.mappings().fetchmany()
    return {"count": len(res), "success": True}


async def get_subscribers(user_id: int):
    async with async_session_factory() as session:
        stmt = (
            select(UserProfile.user_id, UserProfile.nickname, UserProfile.avatar_link)
            .join_from(
                UserSubscribers,
                UserProfile,
                UserSubscribers.subscribers_id == UserProfile.user_id,
            )
            .where(UserSubscribers.user_id == user_id)
        )
        data = await session.execute(stmt)
        res = data.mappings().fetchmany()
    return res


async def subscribers_count(user_id: int):
    async with async_session_factory() as session:
        stmt = (
            select(UserProfile.user_id)
            .join_from(
                UserSubscribers,
                UserProfile,
                UserSubscribers.subscribers_id == UserProfile.user_id,
            )
            .where(UserSubscribers.user_id == user_id)
        )
        data = await session.execute(stmt)
        res = data.mappings().fetchmany()
    return {"count": len(res), "success": True}


async def add_to_subscribers_table(user_id: int, subscriber_id: int):
    async with async_session_factory() as session:
        data = {"user_id": user_id, "subscribers_id": subscriber_id}
        stmt = UserSubscribers(**data)
        session.add(stmt)
        await session.flush()
        await session.commit()
    return {"success": True}


async def add_post(
    post_id: str,
    user_id: int,
    description: str,
    files: list[UploadFile],
    file_link: list[str],
):
    async with async_session_factory() as session:
        data1 = {
            "post_id": post_id,
            "user_id": user_id,
            "desscription": description,
        }
        stmt1 = Posts(**data1)
        session.add(stmt1)
        await session.flush()
        await session.commit()
        stmt2 = select(Posts.id).where(Posts.post_id == post_id)
        data = await session.execute(stmt2)
        post_id_fkey = data.scalar()
        i = 0
        for file in files:
            data2 = {
                "post_id_fkey": post_id_fkey,
                "post_id": post_id,
                "file_name": file.filename,
                "file_link": file_link[i],
                "file_weight": file.size,
            }
            i += 1
            stmt3 = Photos(**data2)
            session.add(stmt3)
            await session.flush()
        await session.commit()
    return {"success": True}


async def create_comment_post(post_id: int, user_id: int, comment_text: str):
    async with async_session_factory() as session:
        data = {
            "post_id": post_id,
            "user_id": user_id,
            "comment_text": comment_text,
        }
        stmt = Comments(**data)
        session.add(stmt)
        await session.flush()
        await session.commit()
    return {"success": True}


async def get_comments_post(post_id: int):
    async with async_session_factory() as session:
        stmt = (
            select(
                Comments.post_id,
                Comments.comment_text,
                UserProfile.user_id,
                UserProfile.nickname,
                UserProfile.avatar_link,
                Comments.created_at,
            )
            .join_from(Comments, UserProfile, Comments.user_id == UserProfile.user_id)
            .where(Comments.post_id == post_id)
        )
        data = await session.execute(stmt)
        res = data.mappings().fetchmany()
    return res


async def get_users_posts(user_id: int, posts_limit: int, page: int):
    async with async_session_factory() as session:
        comment_subq = (
            select(func.count(Comments.post_id))
            .where(Comments.post_id == Posts.id, Posts.user_id == user_id)
            .scalar_subquery()
        )
        likes_subq = (
            select(func.count(Likes.post_id))
            .where(Likes.post_id == Posts.id, Posts.user_id == user_id)
            .scalar_subquery()
        )
        stmt1 = (
            select(
                Posts.id,
                Posts.user_id,
                Posts.desscription,
                Posts.posted_at,
                func.array_agg(Photos.file_link).label("photo_links"),
                likes_subq.label("likes_count"),
                comment_subq.label("comments_count"),
            )
            .join_from(Posts, Photos, Posts.id == Photos.post_id_fkey)
            .where(
                Posts.user_id == user_id,
            )
            .group_by(Posts.id)
            .order_by(desc(Posts.posted_at))
            .limit(posts_limit)
        )
        data = await session.execute(stmt1)
        res = data.mappings().fetchmany()
        return res


async def like_post(post_id: int, user_id: int):
    async with async_session_factory() as session:
        stmt = select(Likes).where(Likes.post_id == post_id, Likes.user_id == user_id)
        res = await session.execute(stmt)
        if res.scalar() is None:
            data = {
                "post_id": post_id,
                "user_id": user_id,
            }
            stmt1 = Likes(**data)
            session.add(stmt1)
            await session.flush()
            await session.commit()
            return {"success": True, "action": "like"}
        else:
            stmt2 = delete(Likes).where(
                Likes.post_id == post_id, Likes.user_id == user_id
            )
            await session.execute(stmt2)
            await session.flush()
            await session.commit()
            return {"success": True, "action": "dislike"}


# sd
# CHAT OPERATION
async def get_messages_between_users(user_id_1: int, user_id_2: int):
    async with async_session_factory() as session:
        stmt = select(
            Messages.sender_id,
            Messages.recipient_id,
            Messages.content,
            Messages.send_time,
        ).filter(
            or_(
                and_(
                    Messages.recipient_id == user_id_1, Messages.sender_id == user_id_2
                ),
                and_(
                    Messages.recipient_id == user_id_2, Messages.sender_id == user_id_1
                ),
            )
        )
        data = await session.execute(stmt)
        res = data.mappings().fetchmany()
        return res


async def create_message(sender_id: int, recipient_id: int, content: str):
    async with async_session_factory() as session:
        data = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "content": content,
        }
        stmt = Messages(**data)
        session.add(stmt)
        await session.flush()
        await session.commit()
        return {"success": True}


# PASSWORD OPERATION


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_password)
