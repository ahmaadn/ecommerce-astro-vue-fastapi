from datetime import datetime, timedelta
from typing import Literal

from email_validator import EmailNotValidError, validate_email
from fastapi import Depends, HTTPException, status
from fastapi.requests import HTTPConnection
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
)

from app.config import get_settings
from app.database import DependsDB, get_db
from app.users.models import User
from app.users.services import get_user_by_email, get_user_by_username

from .schemas import JWTCreds, JWTMeta, JWTPayload
from .security import verify_password

API_VERSION = get_settings().API_VERSION
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_VERSION}/auth/token")


class Authentication:
    @classmethod
    def create_access_token(
        cls,
        user: User,
        expires_time: int = get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> str:
        jwt_meta = JWTMeta(
            iat=datetime.timestamp(datetime.now()),
            exp=datetime.timestamp(datetime.now() + timedelta(minutes=expires_time)),
        )
        jwt_crid = JWTCreds(
            sub=str(user.email), username=str(user.username), permission=user.role.name
        )
        token_playload = JWTPayload(
            **jwt_meta.model_dump(),
            **jwt_crid.model_dump(),
        )
        return jwt.encode(
            token_playload.model_dump(), get_settings().JWT_SECRET_KEY, get_settings().JWT_ALGORITHM
        )

    @classmethod
    async def get_user_by_email_or_username(cls, db: Session, username: str) -> User | None:
        try:
            valid = validate_email(username, test_environment=get_settings().DEBUG_MODE)
            email = valid.email
            user = await get_user_by_email(db, email)
            return user
        except EmailNotValidError:
            pass

        user = await get_user_by_username(db, username)
        return user

    @classmethod
    async def authenticate_user(
        cls, db: Session, username: str, password: str
    ) -> User | Literal[False]:
        user = await Authentication.get_user_by_email_or_username(db, username)
        if user is None:
            return False
        if not verify_password(
            password=password, salt=str(user.salt), hashed_pw=str(user.password)
        ):
            return False
        return user

    @classmethod
    async def get_current_user(cls, db: DependsDB, token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token_playload = jwt.decode(
                token, get_settings().JWT_SECRET_KEY, [get_settings().JWT_ALGORITHM]
            )
            jwt_crid = JWTCreds(**token_playload)
            username = jwt_crid.username
        except (JWTError, ValidationError):
            raise credentials_exception

        user = await get_user_by_username(db, username)
        if user is None:
            raise credentials_exception
        return user


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser]:
        guest = AuthCredentials(["unauthenticated"]), UnauthenticatedUser()

        if "authorization" not in conn.headers:
            return guest

        token = conn.headers.get("authorization").split(" ")[1]  # type: ignore
        db = next(get_db())
        user = await Authentication.get_current_user(db, token)
        return AuthCredentials("authenticated"), user  # type: ignore
