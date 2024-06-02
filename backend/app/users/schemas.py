from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from .enums import RoleEnum


class UserBase(BaseModel):
    nama: str = Field(max_length=100)
    username: str = Field(max_length=100)
    email: EmailStr
    no_hp: str | None = Field(default=None, max_length=20)


class UserCreateModel(UserBase):
    password: str = Field(min_length=8)


class UserPublic(UserBase):
    is_aktif: bool
    role: RoleEnum

    dibuat_at: datetime
    diupdate_at: datetime


class PasswordUpdateModel(BaseModel):
    password: str = Field(min_length=8)
    salt: str


class UpdateUserModel(BaseModel):
    nama: str | None = Field(default=None, max_length=100)
    username: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None)
    no_hp: str | None = Field(default=None, max_length=20)
    is_aktif: bool | None = Field(default=None)
    role: RoleEnum | None = Field(default=None)


class PasswordUpdateRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=8)
