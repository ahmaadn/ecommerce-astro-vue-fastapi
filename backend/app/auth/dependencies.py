from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.users.enums import RoleEnum
from app.users.models import User

from .authentication import Authentication


def get_current_active_user(
    current_user: Annotated[User, Depends(Authentication.get_current_user)],
):
    if not current_user.is_aktif:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_admin(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if not current_user or current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have not enough privileges",
        )
    return current_user


is_user_active = Annotated[User, Depends(get_current_active_user)]
is_user_admin = Annotated[User, Depends(get_current_active_admin)]
