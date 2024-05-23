from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.auth.security import create_salt_and_hashed_password

from .models import User
from .schemas import UserCreateModel


async def get_user_by_email(db: Session, email: EmailStr) -> User | None:
    user_db = db.query(User).where(User.email == email).first()
    if user_db is None:
        return None
    return user_db


async def get_user_by_username(db: Session, username: str) -> User | None:
    user_db = db.query(User).where(User.username == username).first()
    if user_db is None:
        return None
    return user_db


async def create_new_user(db: Session, user: UserCreateModel) -> User:
    user_db = await get_user_by_email(db, user.email)
    if user_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "email already in use")

    user_db = await get_user_by_username(db, user.username)
    if user_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "username already in use")

    new_password = create_salt_and_hashed_password(password=user.password)
    new_user = User(
        nama=user.nama,
        email=user.email,
        username=user.username,
        password=new_password.password,
        salt=new_password.salt,
        no_hp=user.no_hp,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
