import pytest
from datetime import datetime, timezone
from jose import jwt
from app.services.auth import (
    _create_access_token,
    _create_refresh_token,
    create_token_pair,
    decode_access_token,
    refresh_token_state,
    authenticate,
    get_token_of_auth_user,
    SUB, EXP, JTI, IAT
)
from app.schemas.user_schema import UserBase
from app.models.user import User
from app.models.blacklisted_model import BlacklistedToken
from app.config import settings
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials


class TestAuthService:
    """Test authentication service functionality."""
    
    def test_create_access_token(self):
        """Test access token creation."""
        payload = {SUB: "test@example.com", JTI: "test-jti", IAT: datetime.now(timezone.utc)}
        token = _create_access_token(payload)
        
        assert token.token is not None
        assert token.expire is not None
        assert token.payload[SUB] == "test@example.com"
    
    def test_create_access_token_with_custom_minutes(self):
        """Test access token creation with custom expiry."""
        payload = {SUB: "test@example.com", JTI: "test-jti", IAT: datetime.now(timezone.utc)}
        token = _create_access_token(payload, minutes=60)
        
        assert token.token is not None
        assert token.expire is not None
    
    def test_create_refresh_token(self):
        """Test refresh token creation."""
        payload = {SUB: "test@example.com", JTI: "test-jti", IAT: datetime.now(timezone.utc)}
        token = _create_refresh_token(payload)
        
        assert token.token is not None
        assert token.expire is not None
        assert token.payload[SUB] == "test@example.com"
    
    def test_create_token_pair(self):
        """Test token pair creation."""
        user = UserBase(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            age=25
        )
        token_pair = create_token_pair(user)
        
        assert token_pair.access is not None
        assert token_pair.refresh is not None
        assert token_pair.access.token is not None
        assert token_pair.refresh.token is not None
    
    @pytest.mark.asyncio
    async def test_decode_access_token(self, test_db):
        """Test decoding a valid access token."""
        payload = {SUB: "test@example.com", JTI: "test-jti-123", IAT: datetime.now(timezone.utc)}
        token = _create_access_token(payload)
        
        decoded = await decode_access_token(token.token, test_db)
        
        assert decoded[SUB] == "test@example.com"
        assert decoded[JTI] == "test-jti-123"
    
    @pytest.mark.asyncio
    async def test_decode_access_token_invalid(self, test_db):
        """Test decoding an invalid token."""
        with pytest.raises(HTTPException) as exc_info:
            await decode_access_token("invalid_token", test_db)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_decode_access_token_blacklisted(self, test_db):
        """Test decoding a blacklisted token."""
        payload = {SUB: "test@example.com", JTI: "blacklisted-jti", IAT: datetime.now(timezone.utc)}
        token = _create_access_token(payload)
        
        # Add token to blacklist
        blacklisted = BlacklistedToken(
            id="blacklisted-jti",
            expire=datetime.now(timezone.utc)
        )
        test_db.add(blacklisted)
        await test_db.commit()
        
        with pytest.raises(HTTPException) as exc_info:
            await decode_access_token(token.token, test_db)
        
        assert exc_info.value.status_code == 401
    
    def test_refresh_token_state(self):
        """Test refreshing token state."""
        payload = {SUB: "test@example.com", JTI: "test-jti", IAT: datetime.now(timezone.utc)}
        token = _create_refresh_token(payload)
        
        result = refresh_token_state(token.token)
        
        assert "token" in result
        assert result["token"] is not None
    
    def test_refresh_token_state_invalid(self):
        """Test refreshing with invalid token."""
        from app.exceptions.http_exceptions import AuthFailedException
        
        with pytest.raises(AuthFailedException):
            refresh_token_state("invalid_token")
    
    @pytest.mark.asyncio
    async def test_authenticate_success(self, test_db, test_user):
        """Test successful authentication."""
        user = await authenticate(
            email=test_user.email,
            password="testpassword123",
            db=test_db
        )
        
        assert user is not None
        assert user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_authenticate_wrong_password(self, test_db, test_user):
        """Test authentication with wrong password."""
        user = await authenticate(
            email=test_user.email,
            password="wrongpassword",
            db=test_db
        )
        
        assert user is False
    
    @pytest.mark.asyncio
    async def test_authenticate_nonexistent_user(self, test_db):
        """Test authentication with non-existent user."""
        user = await authenticate(
            email="nonexistent@example.com",
            password="password",
            db=test_db
        )
        
        assert user is False
    
    def test_get_token_of_auth_user(self):
        """Test extracting token from credentials."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="test_token_123"
        )
        
        token = get_token_of_auth_user(credentials)
        
        assert token == "test_token_123"
