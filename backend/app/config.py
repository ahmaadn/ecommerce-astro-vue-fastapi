from pydantic import EmailStr, MySQLDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str
    DEBUG_MODE: bool = True
    API_VERSION: str = "/v1"
    STATIC_MEDIA_URL: str = "/static/uploads"

    # mysql database
    MYSQL_SERVER: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USERNAME,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DATABASE,
        )  # type: ignore

    # jwt
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_TOKEN_PREFIX: str

    # admin acount
    INIT_ADMIN_USERNAME: str
    INIT_ADMIN_PASSWORD: str
    INIT_ADMIN_EMAIL: EmailStr


def _singleton(cls):
    _instances = {}

    def warp():
        if cls not in _instances:
            _instances[cls] = cls()
        return _instances[cls]

    return warp


Settings = _singleton(Settings)  # type: ignore


def get_settings() -> "Settings":
    """mendapatkan setting

    Returns:
        Settings: instance settings
    """
    return Settings()  # type: ignore


if __name__ == "__main__":
    print(get_settings())
