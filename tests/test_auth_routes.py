import pytest
from httpx import AsyncClient


class TestAuthRoutes:
    """Test authentication route endpoints."""
    
    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        response = await client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "age": 25,
                "password": "password123",
                "password_confirm": "password123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["first_name"] == "New"
        assert "password" not in data
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration with duplicate email."""
        response = await client.post(
            "/auth/register",
            json={
                "username": "anotheruser",
                "email": test_user.email,
                "first_name": "Another",
                "last_name": "User",
                "age": 30,
                "password": "password123",
                "password_confirm": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "already exist" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client: AsyncClient, test_user):
        """Test registration with duplicate username."""
        response = await client.post(
            "/auth/register",
            json={
                "username": test_user.username,
                "email": "different@example.com",
                "first_name": "Different",
                "last_name": "User",
                "age": 30,
                "password": "password123",
                "password_confirm": "password123"
            }
        )
        
        assert response.status_code == 409
        assert "already exist" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login."""
        response = await client.post(
            "/auth/login",
            data={
                "username": test_user.email,
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] is not None
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password."""
        response = await client.post(
            "/auth/login",
            data={
                "username": test_user.email,
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 400
        assert "Incorrect email or password" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        response = await client.post(
            "/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_logout_success(self, client: AsyncClient, auth_token: str):
        """Test successful logout."""
        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "msg" in data
        assert "logout" in data["msg"].lower()
    
    @pytest.mark.asyncio
    async def test_logout_no_token(self, client: AsyncClient):
        """Test logout without token."""
        response = await client.post("/auth/logout")
        
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_logout_invalid_token(self, client: AsyncClient):
        """Test logout with invalid token."""
        response = await client.post(
            "/auth/logout",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_logout_twice(self, client: AsyncClient, auth_token: str):
        """Test logging out twice with same token."""
        # First logout
        response1 = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response1.status_code == 200
        
        # Second logout with same token should fail
        response2 = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response2.status_code == 401
    
    @pytest.mark.asyncio
    async def test_protected_data_success(self, client: AsyncClient, auth_token: str, test_user):
        """Test accessing protected data with valid token."""
        response = await client.get(
            "/auth/protected_data",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert test_user.email in str(data)
    
    @pytest.mark.asyncio
    async def test_protected_data_no_token(self, client: AsyncClient):
        """Test accessing protected data without token."""
        response = await client.get("/auth/protected_data")
        
        # Without authorization header, FastAPI returns 401
        assert response.status_code in [401, 403]
    
    @pytest.mark.asyncio
    async def test_protected_data_invalid_token(self, client: AsyncClient):
        """Test accessing protected data with invalid token."""
        response = await client.get(
            "/auth/protected_data",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
