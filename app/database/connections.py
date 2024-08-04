from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

engine = create_async_engine(str(settings.database_url))

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()    




