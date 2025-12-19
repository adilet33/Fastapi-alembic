import pytest
from app.exceptions.http_exceptions import AuthFailedException, BadRequestException, NotFoundException


class TestExceptions:
    """Test custom exception classes."""
    
    def test_auth_failed_exception(self):
        """Test AuthFailedException."""
        exc = AuthFailedException()
        assert exc.status_code == 401
        assert "Authenticate failed" in exc.detail
    
    def test_bad_request_exception_default(self):
        """Test BadRequestException with default message."""
        exc = BadRequestException()
        assert exc.status_code == 400
        assert "Bad request" in exc.detail
    
    def test_bad_request_exception_custom(self):
        """Test BadRequestException with custom message."""
        exc = BadRequestException(detail="Custom error")
        assert exc.status_code == 400
        assert exc.detail == "Custom error"
    
    def test_not_found_exception(self):
        """Test NotFoundException."""
        exc = NotFoundException()
        assert exc.status_code == 404
        assert "Not found" in exc.detail
