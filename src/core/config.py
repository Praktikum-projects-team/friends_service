import os
import datetime

from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    base_dir: str = BASE_DIR
    project_name: str = Field(..., env='PROJECT_NAME')
    host: str = Field(..., env='APP_HOST')
    port: int = Field(..., env='APP_PORT')
    is_debug: bool = Field(..., env='IS_DEBUG')


class AuthConfig(BaseSettings):
    host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')
    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='ACCESS_TOKEN_TTL_IN_MINUTES')
    JWT_REFRESH_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='REFRESH_TOKEN_TTL_IN_DAYS')
    admin_login: str = Field(..., env='AUTH_ADMIN_LOGIN')
    admin_password: str = Field(..., env='AUTH_ADMIN_PASSWORD')

    @property
    def url_verify(self):
        return f'{self.host}/api/v1/user/email_verification'

    @property
    def url_redirect(self):
        return f'{self.host}/api/v1/user/profile'


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    name: str = Field(..., env='POSTGRES_DB')

    @property
    def url_sync(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    @property
    def url_async(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class PostgresAuthConfig(BaseSettings):
    host: str = Field(..., env='POSTGRES_HOST_AUTH')
    port: int = Field(..., env='POSTGRES_PORT_AUTH')
    user: str = Field(..., env='POSTGRES_USER_AUTH')
    password: str = Field(..., env='POSTGRES_PASSWORD_AUTH')
    name: str = Field(..., env='POSTGRES_DB_AUTH')

    @property
    def url_async(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


app_config = AppConfig()  # type: ignore[call-arg]
auth_config = AuthConfig()  # type: ignore[call-arg]
pg_config = PostgresConfig()  # type: ignore[call-arg]
pg_auth_config = PostgresAuthConfig()  # type: ignore[call-arg]
