from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    pg_dsn: str = config('DATABASE_URL')
    secret_key_jwt: str = config('SECRET_KEY')
    algorithm: str = config('ALGORITHM')


settings = Settings()
