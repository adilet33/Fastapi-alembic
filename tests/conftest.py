import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport
import uuid

from app.main import app
from app.database.base_class import Base
from app.database.connections import get_db

# Import all models to ensure they are registered with Base
from app.models.user import User
from app.models.task_model import Task
from app.models.blacklisted_model import BlacklistedToken
from app.services.hash import get_password_hash


# Use SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """Create a fresh database for each test."""
    # Create a file-based SQLite database for tests (memory doesn't work well with async)
    import tempfile
    import os
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db_path = temp_db.name
    temp_db.close()
    
    test_url = f"sqlite+aiosqlite:///{temp_db_path}"
    
    engine = create_async_engine(
        test_url,
        poolclass=NullPool,
        echo=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
    
    # Cleanup
    await engine.dispose()
    
    # Delete temp file
    try:
        os.unlink(temp_db_path)
    except:
        pass


@pytest.fixture(scope="function")
async def client(test_db):
    """Create a test client with database override."""
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user(test_db):
    """Create a test user."""
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        age=25,
        password=get_password_hash("testpassword123"),
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_user2(test_db):
    """Create a second test user."""
    user = User(
        id=uuid.uuid4(),
        username="testuser2",
        email="test2@example.com",
        first_name="Test2",
        last_name="User2",
        age=30,
        password=get_password_hash("testpassword456"),
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
async def auth_token(client, test_user):
    """Get authentication token for test user."""
    response = await client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
async def test_task(test_db, test_user):
    """Create a test task."""
    task = Task(
        id=uuid.uuid4(),
        title="Test Task",
        description="Test task description",
        user_id=test_user.id
    )
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)
    return task
