from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import get_settings
from app.database import DependsDB
from app.users.schemas import UserCreateModel
from app.users.services import create_new_user

from .authentication import Authentication
from .schemas import AccessToken

router = r = APIRouter(
    prefix="/auth", tags=["auth"], responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@r.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    db: DependsDB,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AccessToken:
    user = await Authentication.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authentication.create_access_token(
        user=user, expires_time=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return AccessToken(access_token=access_token, token_type=get_settings().JWT_TOKEN_PREFIX)


@r.post("/register", status_code=status.HTTP_201_CREATED)
async def sign_up(db: DependsDB, new_user: UserCreateModel):
    await create_new_user(db, new_user)
    return {"detail": "account successfully registered"}
