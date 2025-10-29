import pytest
from app.services.hash import get_password_hash, verify_password


class TestHashService:
    """Test password hashing functionality."""
    
    def test_get_password_hash(self):
        """Test password hashing."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
    
    def test_get_password_hash_different_results(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to salting
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty(self):
        """Test password verification with empty password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password("", hashed) is False
    
    def test_hash_empty_password(self):
        """Test hashing empty password."""
        hashed = get_password_hash("")
        assert hashed is not None
        assert len(hashed) > 0
