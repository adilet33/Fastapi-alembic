from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn = 'asyncpg://fastapi:fastapi@localhost:5433/fastapi'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'


settings = Settings()
