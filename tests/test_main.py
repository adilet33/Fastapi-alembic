import pytest
from httpx import AsyncClient


class TestMainApplication:
    """Test main application endpoints."""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello world"
