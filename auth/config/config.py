import os
from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    SECRET_KEY = os.getenv("SECRET_KEY", "top_secret")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "auth_database")

    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

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

    class Config:
        env_file = ".env"


settings = BaseConfig()