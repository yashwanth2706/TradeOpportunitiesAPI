"""
Integration Tests for Trade Opportunities API

End-to-end tests combining multiple features.

Test Coverage:
- Complete user workflow (register → login → analyze)
- Rate limiting with session expiry interaction
- Health endpoint functionality
- Multiple concurrent users
"""

import pytest
import time
from jose import jwt

from app.config import settings
from app.core.session import session_manager
from conftest import client

# Extract config values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
RATE_LIMIT_CAPACITY = settings.RATE_LIMIT_CAPACITY
RATE_LIMIT_REFILL_SECONDS = settings.RATE_LIMIT_REFILL_SECONDS


@pytest.mark.integration
class TestIntegration:
    """Integration tests combining multiple features"""
    
    def test_complete_user_flow(self, mock_data_collector, mock_llm_client):
        """Test complete user flow: register -> login -> analyze"""
        # 1. Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={"username": "flowtest", "password": "testpass123"}
        )
        assert register_response.status_code == 201
        
        # 2. Login (should also work)
        login_response = client.post(
            "/api/v1/auth/token",
            data={"username": "flowtest", "password": "testpass123"}
        )
        assert login_response.status_code == 200
        token2 = login_response.json()["access_token"]
        
        # 3. Use token to analyze
        headers = {"Authorization": f"Bearer {token2}"}
        analyze_response = client.get("/api/v1/analyze/technology", headers=headers)
        assert analyze_response.status_code == 200
        
        data = analyze_response.json()
        assert "sector" in data
        assert "report_markdown" in data
        assert "generated_at" in data
    
    def test_rate_limit_with_session_expiry(
        self, auth_headers, mock_data_collector, mock_llm_client
    ):
        """Test that rate limits work correctly with session management"""
        sectors = ["technology", "pharmaceuticals", "agriculture", "dairy", "automotive"]
        # Exhaust rate limit
        for i in range(RATE_LIMIT_CAPACITY):
            response = client.get(f"/api/v1/analyze/{sectors[i]}", headers=auth_headers)
            assert response.status_code == 200
        
        # Should be rate limited
        response = client.get("/api/v1/analyze/technology", headers=auth_headers)
        assert response.status_code == 429
        
        # Expire the session and refill tokens manually
        token = auth_headers["Authorization"].split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        
        if username in session_manager._sessions:
            # Refill tokens by simulating time passage
            session_manager._sessions[username].rate_limiter.last_refill = time.monotonic() - (RATE_LIMIT_REFILL_SECONDS + 1)
        
        # Should work again
        response = client.get("/api/v1/analyze/pharmaceuticals", headers=auth_headers)
        assert response.status_code == 200
    
    def test_health_endpoint_shows_session_count(self, auth_headers, mock_data_collector, mock_llm_client):
        """Test that health endpoint shows active session count"""
        # Create sessions by making authenticated requests
        client.get("/api/v1/analyze/technology", headers=auth_headers)
        
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "active_sessions" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert isinstance(data["active_sessions"], int)
    
    def test_multiple_users_concurrent_access(
        self, mock_data_collector, mock_llm_client
    ):
        """Test multiple users accessing the API concurrently"""
        # Create 3 users
        users = []
        for i in range(3):
            response = client.post(
                "/api/v1/auth/register",
                json={"username": f"user{i}", "password": f"pass{i}123"}
            )
            users.append(response.json()["access_token"])
        
        # Each user makes requests
        sectors = ["technology", "pharmaceuticals", "agriculture"]
        for i, token in enumerate(users):
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get(f"/api/v1/analyze/{sectors[i]}", headers=headers)
            assert response.status_code == 200
