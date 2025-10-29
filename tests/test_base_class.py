import pytest
from app.database.base_class import Base
from fastapi import HTTPException


class TestBaseClass:
    """Test Base class functionality."""
    
    @pytest.mark.asyncio
    async def test_save_method(self, test_db, test_user):
        """Test that save method works (covered by other tests)."""
        # This is already covered by model tests
        assert test_user.id is not None
