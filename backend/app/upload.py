import os
import uuid

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.config import get_settings

BASEDIR = os.path.dirname(__file__)


async def file_operations(file: UploadFile) -> tuple[bytes, str, str]:
    _, ext = os.path.splitext(file.filename)  # type: ignore
    img_dir = os.path.join(BASEDIR, get_settings().STATIC_MEDIA_URL)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Only .jpeg, .png and .jpg  files allowed",
        )
    return content, ext, img_dir


async def handle_file_upload(file: UploadFile) -> str:
    content, ext, img_dir = await file_operations(file)
    file_name = f"{uuid.uuid4().hex}{ext}"
    async with aiofiles.open(os.path.join(img_dir, file_name), mode="wb") as f:
        await f.write(content)

    return file_name
