import os
import re
import shutil
from fastapi import UploadFile, Request


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
        os.remove(
            f"{avatars_dir}/files/avatars/user_{user_id}_avatar.{"jpeg" or "png"}"
        )
        return {"success": True}
    except OSError as err:
        print(err)
