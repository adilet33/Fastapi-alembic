from pydantic import PostgresDsn
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    pg_dsn: PostgresDsn = 'postgresql+asyncpg://ashimov:password@127.0.0.1:5432/task_db'

settings = Settings()