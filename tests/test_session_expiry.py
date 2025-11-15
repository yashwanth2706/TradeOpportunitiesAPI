"""
Session Expiry Tests for Trade Opportunities API

Tests session lifecycle and expiration handling.

Test Coverage:
- Initial session validity
- Session expiration after timeout
- Session validity before timeout
- Expired session recreation
- Session initialization (capacity, tokens)
"""

import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.config import settings
from app.core.session import SessionInfo, session_manager
from conftest import client

# Extract config values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
RATE_LIMIT_CAPACITY = settings.RATE_LIMIT_CAPACITY


@pytest.mark.session
class TestSessionExpiry:
    """Test session expiry functionality"""
    
    def test_session_is_not_expired_initially(self):
        """Test that new sessions are not expired"""
        session = SessionInfo(client_id="testuser")
        assert session.is_expired() is False
    
    def test_session_expires_after_timeout(self):
        """Test that session expires after the timeout period"""
        session = SessionInfo(client_id="testuser")
        
        # Manually set created_at to past time
        session.created_at = datetime.now(timezone.utc) - timedelta(
            seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60 + 1
        )
        
        assert session.is_expired() is True
    
    def test_session_not_expired_before_timeout(self):
        """Test that session doesn't expire before timeout"""
        session = SessionInfo(client_id="testuser")
        
        # Set to just before expiry
        session.created_at = datetime.now(timezone.utc) - timedelta(
            seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60 - 10
        )
        
        assert session.is_expired() is False
    
    def test_expired_session_requires_relogin(
        self, test_user, mock_data_collector, mock_llm_client
    ):
        """Test that expired sessions require re-login"""
        # Get a fresh token for this test
        response = client.post(
            "/api/v1/auth/token",
            data={"username": test_user["username"], "password": test_user["password"]}
        )
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Make a request to create session
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 200
        
        # Get the username from token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        
        # Verify session exists
        assert username in session_manager._sessions
        
        # Manually expire the session (but token is still valid)
        session_manager._sessions[username].created_at = datetime.now(timezone.utc) - timedelta(
            seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60 + 1
        )
        
        # Make another request - should be rejected with 401
        response = client.get("/api/v1/analyze/pharmaceuticals", headers=headers)
        assert response.status_code == 401
        assert "session expired" in response.json()["detail"].lower()
        
        # Session should be removed
        assert username not in session_manager._sessions
    
    def test_session_capacity_and_tokens_initialized(self):
        """Test that session is initialized with correct capacity"""
        session = SessionInfo(client_id="testuser")
        
        assert session.rate_limiter.capacity == RATE_LIMIT_CAPACITY
        assert session.rate_limiter.tokens == RATE_LIMIT_CAPACITY
        assert session.usage_count == 0
