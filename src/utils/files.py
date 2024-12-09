import os
import re
import shutil

from fastapi import UploadFile


def add_new_file(files: list[UploadFile], post_id: str):
    print(len(files))
    try:
        if len(files) > 10:
            raise ValueError("максимум 10 фотографий")
        for file in files:
            if file.size > 31457280:
                raise ValueError("размер фото не должен превышать 30 мб")
        links = []
        post_dir = f"../Files/Photos/{post_id}"
        os.makedirs(post_dir)
        for file in files:
            file.filename = f"file_{file.size}_{post_id}_post.{(re.search(r"(jpeg)|(png)", file.content_type)).group()}"
            links.append(post_dir + "/" + file.filename)
            with open(post_dir + "/" + file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        return {"success": True, "links": links}
    except ValueError as error:
        return {"success": False, "msg": error}
