import pytest
from backend.core.identity.auth.service import AuthService
from backend.core.identity.auth.models import User

def test_password_hashing():
    """Test password is properly hashed."""
    service = AuthService()
    hashed = service.hash_password('test123')
    assert hashed != 'test123'
    assert service.verify_password('test123', hashed)

def test_permission_logic():
    """Test role-based permission logic."""
    service = AuthService()
    # Admin should have all permissions
    assert service.has_permission('admin', 'any.permission') is True
    # Counselor should have specific permissions
    assert service.has_permission('danisman', 'portfolio.view') is True
    assert service.has_permission('danisman', 'finance.manage') is False
