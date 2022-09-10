import os
from pydantic import BaseSettings, Field, BaseModel

from dotenv import load_dotenv

load_dotenv()


class BaseConfig(BaseSettings):
    SECRET_KEY: str = Field("top_secret", env="SECRET_KEY")

    POSTGRES_HOST: str = Field("127.0.0.1", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("123456", env="POSTGRES_PASSWORD")
    POSTGRES_DATABASE: str = Field("auth_database", env="POSTGRES_DATABASE")

    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")

    OAUTH_CREDENTIALS = {
        'google': {
            'client_id': os.environ["GOOGLE_OAUTH_ID"],
            'client_secret': os.environ["GOOGLE_OAUTH_SECRET"],
            'authorize_url': 'https://accounts.google.com/',
            'access_token_url': 'https://oauth2.googleapis.com/token',
            'base_url': 'https://www.googleapis.com/oauth2/v1/'
        },
        'yandex': {
            'client_id': os.environ["YANDEX_OAUTH_ID"],
            'client_secret': os.environ["YANDEX_OAUTH_SECRET"],
            'authorize_url': 'https://oauth.yandex.ru/authorize',
            'access_token_url': 'https://oauth.yandex.ru/token',
            'base_url': 'https://login.yandex.ru/',

        },
    }


settings = BaseConfig()