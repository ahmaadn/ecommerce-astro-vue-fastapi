import bcrypt
from passlib.context import CryptContext

from app.users.schemas import PasswordUpdateModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_salt_and_hashed_password(*, password: str):
    salt = generate_salt()
    hash_password = hashed_password(password=password, salt=salt)
    return PasswordUpdateModel(password=hash_password, salt=salt)


def generate_salt():
    return bcrypt.gensalt().decode()


def hashed_password(*, password: str, salt: str):
    return pwd_context.hash(password + salt)


def verify_password(*, password: str, salt: str, hashed_pw: str):
    return pwd_context.verify(password + salt, hashed_pw)
