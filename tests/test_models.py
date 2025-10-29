import pytest
import uuid
from app.models.user import User
from app.models.task_model import Task
from app.models.blacklisted_model import BlacklistedToken
from app.services.hash import get_password_hash
from datetime import datetime, timezone


class TestUserModel:
    """Test User model functionality."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, test_db):
        """Test creating a user."""
        user = User(
            id=uuid.uuid4(),
            username="newuser",
            email="newuser@example.com",
            first_name="New",
            last_name="User",
            age=28,
            password=get_password_hash("password123"),
            is_active=True
        )
        test_db.add(user)
        await test_db.commit()
        await test_db.refresh(user)
        
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.age == 28
    
    @pytest.mark.asyncio
    async def test_find_by_email(self, test_db, test_user):
        """Test finding user by email."""
        found_user = await User.find_by_email(db=test_db, email=test_user.email)
        
        assert found_user is not None
        assert found_user.id == test_user.id
        assert found_user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_find_by_email_not_found(self, test_db):
        """Test finding non-existent user by email."""
        found_user = await User.find_by_email(db=test_db, email="nonexistent@example.com")
        
        assert found_user is None
    
    @pytest.mark.asyncio
    async def test_find_by_username(self, test_db, test_user):
        """Test finding user by username."""
        found_user = await User.find_by_username(db=test_db, username=test_user.username)
        
        assert found_user is not None
        assert found_user.id == test_user.id
        assert found_user.username == test_user.username
    
    @pytest.mark.asyncio
    async def test_find_by_username_not_found(self, test_db):
        """Test finding non-existent user by username."""
        found_user = await User.find_by_username(db=test_db, username="nonexistent")
        
        assert found_user is None
    
    @pytest.mark.asyncio
    async def test_user_task_relationship(self, test_db, test_user):
        """Test user-task relationship."""
        task = Task(
            id=uuid.uuid4(),
            title="Test Task",
            description="Test description",
            user_id=test_user.id
        )
        test_db.add(task)
        await test_db.commit()
        
        # Refresh to load relationships
        await test_db.refresh(test_user, attribute_names=['tasks'])
        
        assert len(test_user.tasks) > 0
        assert test_user.tasks[0].title == "Test Task"


class TestTaskModel:
    """Test Task model functionality."""
    
    @pytest.mark.asyncio
    async def test_create_task(self, test_db, test_user):
        """Test creating a task."""
        task = Task(
            id=uuid.uuid4(),
            title="New Task",
            description="New task description",
            user_id=test_user.id
        )
        test_db.add(task)
        await test_db.commit()
        await test_db.refresh(task)
        
        assert task.id is not None
        assert task.title == "New Task"
        assert task.description == "New task description"
        assert task.user_id == test_user.id
    
    @pytest.mark.asyncio
    async def test_find_by_user(self, test_db, test_user):
        """Test finding tasks by user."""
        # Create multiple tasks
        for i in range(3):
            task = Task(
                id=uuid.uuid4(),
                title=f"Task {i}",
                description=f"Description {i}",
                user_id=test_user.id
            )
            test_db.add(task)
        await test_db.commit()
        
        tasks = await Task.find_by_user(db=test_db, user=test_user)
        
        assert len(tasks) == 3
        assert all(task.user_id == test_user.id for task in tasks)
    
    @pytest.mark.asyncio
    async def test_find_by_user_no_tasks(self, test_db, test_user2):
        """Test finding tasks for user with no tasks."""
        tasks = await Task.find_by_user(db=test_db, user=test_user2)
        
        assert len(tasks) == 0


class TestBlacklistedTokenModel:
    """Test BlacklistedToken model functionality."""
    
    @pytest.mark.asyncio
    async def test_create_blacklisted_token(self, test_db):
        """Test creating a blacklisted token."""
        token = BlacklistedToken(
            id="test-token-id",
            expire=datetime.now(timezone.utc)
        )
        await token.save(db=test_db)
        
        assert token.id == "test-token-id"
    
    @pytest.mark.asyncio
    async def test_find_by_id(self, test_db):
        """Test finding blacklisted token by ID."""
        token_id = "test-token-id-123"
        token = BlacklistedToken(
            id=token_id,
            expire=datetime.now(timezone.utc)
        )
        await token.save(db=test_db)
        
        found_token = await BlacklistedToken.find_by_id(db=test_db, id=token_id)
        
        assert found_token is not None
        assert found_token.id == token_id
    
    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, test_db):
        """Test finding non-existent blacklisted token."""
        found_token = await BlacklistedToken.find_by_id(db=test_db, id="nonexistent")
        
        assert found_token is None
