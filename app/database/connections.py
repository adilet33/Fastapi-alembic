from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

engine = create_async_engine(str(settings.pg_dsn))

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_async_session():
    async with async_session_maker() as session:
        yield session