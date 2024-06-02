from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func

from app.database import Base

from .enums import RoleEnum


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    salt = Column(String(100), nullable=False)
    no_hp = Column(String(20), default=None)
    is_aktif = Column(Boolean, default=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)

    dibuat_at = Column(DateTime, default=datetime.now(UTC), server_default=func.now())
    diupdate_at = Column(DateTime, default=datetime.now(UTC), onupdate=func.now())
