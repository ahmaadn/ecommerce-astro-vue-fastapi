from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from app.auth.dependencies import get_current_active_admin, is_user_active
from app.auth.security import create_salt_and_hashed_password, verify_password
from app.config import get_settings
from app.database import DependsDB

from .enums import RoleEnum
from .models import User
from .schemas import PasswordUpdateRequest, UpdateUserModel, UserPublic
from .services import get_user_by_username

router = r = APIRouter(prefix="/users", tags=["users"])


@r.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def get_user_by_id(current_user: is_user_active):
    return current_user


@r.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Page[UserPublic],
    dependencies=[Depends(get_current_active_admin)],
)
async def get_users(db: DependsDB):
    return paginate(db, select(User).order_by(User.dibuat_at))


@r.get(
    "/details",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_admin)],
)
async def get_user(db: DependsDB, username: str):
    user_db = await get_user_by_username(db, username)
    if not user_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user tidak ditemukan")
    return user_db


@r.put("", status_code=status.HTTP_200_OK)
async def update_users(
    db: DependsDB, current_user: is_user_active, username: str, new_data: UpdateUserModel
):
    if (
        current_user.role != RoleEnum.ADMIN
        or current_user.username != username
        and current_user.role == RoleEnum.USER
    ):
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "Tidak punyak hak akses")

    # user_db =
    if current_user.username == username:  # type: ignore
        user_db = current_user
    else:
        user_db = await get_user_by_username(db, username)
        if not user_db:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user tidak ditemukan")

    # Cek email sudah dipakai
    if new_data.email:
        email_user_db = (
            db.query(User)
            .where(User.email == new_data.email, User.user_id != user_db.user_id)
            .first()
        )
        if email_user_db:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "email already in use")

        try:
            validate_email(new_data.email, test_environment=get_settings().DEBUG_MODE)
        except EmailNotValidError as e:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "email tidak valid") from e

    # Cek username sudah dipakai
    if new_data.username:
        email_user_db = (
            db.query(User)
            .where(User.username == new_data.username, User.user_id != user_db.user_id)
            .first()
        )
        if email_user_db:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "email already in use")

    # Cek menggganti role
    if new_data.role and user_db.role == RoleEnum.ADMIN and new_data.role == RoleEnum.USER:  # type: ignore
        other_admin_db = (
            db.query(User)
            .where(User.role == new_data.role, User.user_id != user_db.user_id)
            .first()
        )

        if not other_admin_db:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Tidak bisa mengganti role admin")

    for field, value in new_data.model_dump(exclude_none=True).items():
        setattr(user_db, field, value)

    db.commit()
    db.refresh(user_db)
    return {"detail": "user berhasil di update"}


@r.post("/new-password", status_code=status.HTTP_200_OK)
def set_new_password(db: DependsDB, current_user: is_user_active, password: PasswordUpdateRequest):
    is_valid = verify_password(
        password=password.password,
        salt=str(current_user.salt),
        hashed_pw=str(current_user.password),
    )
    if not is_valid:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "password tidak sama")

    new_pass = create_salt_and_hashed_password(password=password.new_password)

    current_user.password = new_pass.password
    current_user.salt = new_pass.salt
    db.commit()
    db.refresh(current_user)
    return {"detail": "Mengganti password selesai"}
