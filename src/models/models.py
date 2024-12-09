from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text, ForeignKey
from typing import Annotated

import datetime

intpk = Annotated[int, mapped_column(unique=True, primary_key=True)]


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    # user_profile: Mapped[relationship("UserProfile")] = relationship(
    #     back_populates="user"
    # )
    #
    # user_protect_data: Mapped[relationship("User")] = relationship(
    #     back_populates="user"
    # )


class UserProtect(Base):
    __tablename__ = "users_protect"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    long_hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    short_hashed_password: Mapped[str] = mapped_column(nullable=False)

    # user: Mapped[relationship("UserProtect")] = relationship(
    #     back_populates="user_protect_data", single_parent=True
    # )
    #


class UserRefreshToken(Base):
    __tablename__ = "users_refresh_tokens"
    id: Mapped[intpk]
    user_id_refresh: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    token_id: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str] = mapped_column(nullable=False)


class UserProfile(Base):
    __tablename__ = "users_profiles"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user_profile_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(nullable=True)
    nickname: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    avatar_link: Mapped[str] = mapped_column(nullable=True)
    private_account: Mapped[bool] = mapped_column(default=True)

    # user_subscribers: Mapped[relationship("UserSubscribes")] = relationship(
    #     back_populates="users"
    # )
    # #
    # user_subscribers: Mapped[relationship("UserSubscribers")] = relationship(
    #     back_populates="user_profile",
    #     primaryjoin="and_UserProfile.id ==  UserSubscribers.user_id",
    # )


class UserSubscribers(Base):
    __tablename__ = "user_subscribers"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_profiles.id", ondelete="CASCADE")
    )
    subscribers_id: Mapped[int]
    sub_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    #
    # user_profile: Mapped[relationship("UserProfile")] = relationship(
    #     back_populates="user_subscribers",
    # )


class UserSubscribes(Base):
    __tablename__ = "user_subscribes"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_profiles.id", ondelete="CASCADE")
    )
    subscribes_id: Mapped[int]
    sub_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    # subscribes: Mapped[relationship("UserProfile")] = relationship(
    #     back_populates="user_subscribes"
    # )


class Posts(Base):
    __tablename__ = "users_posts"
    id: Mapped[intpk]
    post_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_profiles.id", ondelete="CASCADE")
    )
    desscription: Mapped[str] = mapped_column(String(2200), nullable=True)
    posted_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )


class Photos(Base):
    __tablename__ = "users_photos"
    id: Mapped[intpk]
    post_id_fkey: Mapped[int] = mapped_column(
        ForeignKey("users_posts.id", ondelete="CASCADE")
    )
    post_id: Mapped[str]
    file_name: Mapped[str]
    file_link: Mapped[str]
    file_weight: Mapped[int]
