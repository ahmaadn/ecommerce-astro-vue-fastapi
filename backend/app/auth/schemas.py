from datetime import datetime, timedelta

from pydantic import EmailStr

from app.config import get_settings
from app.schemas import CoreModel


class JWTMeta(CoreModel):
    iat: float = datetime.timestamp(datetime.now())
    exp: float = datetime.timestamp(
        datetime.now() + timedelta(minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )


class JWTCreds(CoreModel):
    """How we'll identify users"""

    sub: EmailStr
    username: str
    permission: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    Informasi terkait JWT : https://datatracker.ietf.org/doc/html/rfc7519#section-4.1
    """


class AccessToken(CoreModel):
    access_token: str
    token_type: str
