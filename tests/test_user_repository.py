import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.repository.user import create_user, create_token_for_user
from app.schemas.user_schema import UserCreate


class TestUserRepository:
    """Test user repository functions."""
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, test_db):
        """Test creating a new user."""
        user_data = UserCreate(
            username="repouser",
            email="repouser@example.com",
            first_name="Repo",
            last_name="User",
            age=28,
            password="password123",
            password_confirm="password123"
        )
        
        new_user = await create_user(body=user_data, db=test_db)
        
        assert new_user is not None
        assert new_user.email == "repouser@example.com"
        assert new_user.first_name == "Repo"
        assert "password" not in new_user.model_dump()
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, test_db, test_user):
        """Test creating user with duplicate email."""
        user_data = UserCreate(
            username="newusername",
            email=test_user.email,
            first_name="New",
            last_name="User",
            age=25,
            password="password123",
            password_confirm="password123"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await create_user(body=user_data, db=test_db)
        
        assert exc_info.value.status_code == 400
        assert "already exist" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_username(self, test_db, test_user):
        """Test creating user with duplicate username."""
        user_data = UserCreate(
            username=test_user.username,
            email="newemail@example.com",
            first_name="New",
            last_name="User",
            age=25,
            password="password123",
            password_confirm="password123"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await create_user(body=user_data, db=test_db)
        
        assert exc_info.value.status_code == 409
        assert "already exist" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_create_token_for_user_success(self, test_db, test_user):
        """Test creating token for valid user."""
        # Mock OAuth2PasswordRequestForm
        class MockForm:
            username = test_user.email
            password = "testpassword123"
        
        form = MockForm()
        token_response = await create_token_for_user(body=form, db=test_db)
        
        assert "access_token" in token_response
        assert token_response["access_token"] is not None
    
    @pytest.mark.asyncio
    async def test_create_token_for_user_wrong_password(self, test_db, test_user):
        """Test creating token with wrong password."""
        from app.exceptions.http_exceptions import BadRequestException
        
        class MockForm:
            username = test_user.email
            password = "wrongpassword"
        
        form = MockForm()
        
        with pytest.raises(BadRequestException):
            await create_token_for_user(body=form, db=test_db)
    
    @pytest.mark.asyncio
    async def test_create_token_for_user_nonexistent(self, test_db):
        """Test creating token for non-existent user."""
        from app.exceptions.http_exceptions import BadRequestException
        
        class MockForm:
            username = "nonexistent@example.com"
            password = "password123"
        
        form = MockForm()
        
        with pytest.raises(BadRequestException):
            await create_token_for_user(body=form, db=test_db)
