"""
Rate Limiting Tests for Trade Opportunities API

Tests the token bucket rate limiting algorithm implementation.

Test Coverage:
- Initial request allowance within capacity
- Request blocking after exceeding limit
- Per-user rate limit isolation
- Token bucket refill mechanism
- Partial time-based refill
- Usage count tracking
"""

import pytest
import time
from fastapi.testclient import TestClient

from app.config import settings
from app.core.session import SessionInfo
from conftest import client

# Extract config values
RATE_LIMIT_CAPACITY = settings.RATE_LIMIT_CAPACITY
RATE_LIMIT_REFILL_SECONDS = settings.RATE_LIMIT_REFILL_SECONDS


@pytest.mark.ratelimit
class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_allows_initial_requests(
        self, auth_headers, mock_data_collector, mock_llm_client
    ):
        """Test that initial requests within limit are allowed"""
        # Valid sector names without numbers
        sectors = ["technology", "pharmaceuticals", "agriculture", "dairy", "automotive"]
        # Should be able to make RATE_LIMIT_CAPACITY requests
        for i in range(RATE_LIMIT_CAPACITY):
            response = client.get(
                f"/api/v1/analyze/{sectors[i % len(sectors)]}",
                headers=auth_headers
            )
            assert response.status_code == 200, f"Request {i+1} failed"
    
    def test_rate_limit_blocks_excess_requests(
        self, auth_headers, mock_data_collector, mock_llm_client
    ):
        """Test that requests exceeding the limit are blocked"""
        sectors = ["technology", "pharmaceuticals", "agriculture", "dairy", "automotive"]
        # Make RATE_LIMIT_CAPACITY requests (should succeed)
        for i in range(RATE_LIMIT_CAPACITY):
            response = client.get(
                f"/api/v1/analyze/{sectors[i]}",
                headers=auth_headers
            )
            assert response.status_code == 200
        
        # Next request should be rate limited
        response = client.get("/api/v1/analyze/technology", headers=auth_headers)
        assert response.status_code == 429
        assert "rate limit" in response.json()["detail"].lower()
    
    def test_rate_limit_per_user(
        self, test_user, mock_data_collector, mock_llm_client
    ):
        """Test that rate limits are enforced per user"""
        # Create two different users
        user1_token = client.post(
            "/api/v1/auth/register",
            json={"username": "user1", "password": "pass123"}
        ).json()["access_token"]
        
        user2_token = client.post(
            "/api/v1/auth/register",
            json={"username": "user2", "password": "pass123"}
        ).json()["access_token"]
        
        # User 1 exhausts their rate limit
        sectors = ["technology", "pharmaceuticals", "agriculture", "dairy", "automotive"]
        for i in range(RATE_LIMIT_CAPACITY):
            response = client.get(
                f"/api/v1/analyze/{sectors[i]}",
                headers={"Authorization": f"Bearer {user1_token}"}
            )
            assert response.status_code == 200
        
        # User 1's next request should be blocked
        response = client.get(
            "/api/v1/analyze/technology",
            headers={"Authorization": f"Bearer {user1_token}"}
        )
        assert response.status_code == 429
        
        # User 2 should still have their full quota
        response = client.get(
            "/api/v1/analyze/pharmaceuticals",
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        assert response.status_code == 200
    
    def test_rate_limit_token_bucket_refill(self):
        """Test that the token bucket refills over time"""
        session = SessionInfo(client_id="testuser")
        
        # Consume all tokens
        for _ in range(RATE_LIMIT_CAPACITY):
            assert session.allow_request() is True
        
        # Next request should be denied
        assert session.allow_request() is False
        
        # Simulate time passing (RATE_LIMIT_REFILL_SECONDS + 1)
        session.rate_limiter.last_refill = time.monotonic() - (RATE_LIMIT_REFILL_SECONDS + 1)
        
        # Should allow requests again
        assert session.allow_request() is True
    
    def test_rate_limit_partial_refill(self):
        """Test partial token refill after partial time passage"""
        session = SessionInfo(client_id="testuser")
        
        # Consume all tokens
        for _ in range(RATE_LIMIT_CAPACITY):
            assert session.allow_request() is True
        
        assert session.allow_request() is False
        
        # Simulate half the refill time passing
        session.rate_limiter.last_refill = time.monotonic() - (RATE_LIMIT_REFILL_SECONDS // 2)
        
        # Should still be blocked (not enough time for full refill)
        assert session.allow_request() is False
        
        # Simulate full refill time
        session.rate_limiter.last_refill = time.monotonic() - RATE_LIMIT_REFILL_SECONDS
        
        # Should now be allowed
        assert session.allow_request() is True
    
    def test_session_info_usage_count(self):
        """Test that usage count is tracked correctly"""
        session = SessionInfo(client_id="testuser")
        
        assert session.usage_count == 0
        
        for i in range(3):
            session.allow_request()
            assert session.usage_count == i + 1
