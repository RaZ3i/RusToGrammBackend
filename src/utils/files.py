import os
import re
import shutil
from fastapi import UploadFile, Request
from pathlib import Path

# from src.service.service import add_avatar_link


def add_new_file(files: list[UploadFile], post_id: str, request: Request):
    try:
        if len(files) > 10:
            raise ValueError("максимум 10 фотографий")
        for file in files:
            if file.size > 31457280:
                raise ValueError("размер фото не должен превышать 30 мб")
        links = []
        post_dir = f"./files/photos/{post_id}"
        os.makedirs(post_dir)
        for file in files:
            file.filename = f"file_{file.size}_{post_id}_post.{(re.search(r"(jpeg)|(png)", file.content_type)).group()}"
            file_link_for_front = request.url_for(
                "media_files", path=f"/photos/{post_id}/" + file.filename
            )
            links.append(str(file_link_for_front))

            with open(post_dir + "/" + file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        return {"success": True, "links": links}
    except ValueError as error:
        return {"success": False, "msg": error.args}


async def delete_user_avatar(user_id: int):
    try:
        avatars_dir = re.sub(r"\\", "/", os.getcwd())
        os.remove(f"{avatars_dir}/files/avatars/user_{user_id}_avatar.jpeg")

        return {"success": True}
    except OSError:
        os.remove(f"{avatars_dir}/files/avatars/user_{user_id}_avatar.png")
    except OSError as err:
        return err


async def add_avatar(avatar: UploadFile, user_id: int, request: Request):
    new_file_name = "/avatars/" + avatar.filename.replace(
        avatar.filename,
        f"user_{user_id}_avatar.{(re.search(r"(jpeg)|(png)", avatar.content_type)).group()}",
    )
    avatars_dir_for_save = (
        Path(__file__).parent.parent
        / f"files/avatars/{avatar.filename.replace(avatar.filename,
                                                       f"user_{user_id}_avatar.{(re.search(r"(jpeg)|(png)", avatar.content_type)).group()}")}"
    )
    avatar_dir_for_front = request.url_for("media_files", path=new_file_name)
    await delete_user_avatar(user_id=user_id)
    with open(avatars_dir_for_save, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)
    return {"success": True, "avatar_link": str(avatar_dir_for_front)}
