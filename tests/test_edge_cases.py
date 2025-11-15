"""
Edge Cases and Error Handling Tests for Trade Opportunities API

Tests edge cases and error handling scenarios.

Test Coverage:
- Malformed authorization headers
- Missing Bearer prefix
- Empty authorization headers
- Invalid JWT signatures
- Missing JWT claims
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from jose import jwt

from app.config import settings
from conftest import client

# Extract config values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


@pytest.mark.edge
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_malformed_authorization_header(self):
        """Test with malformed authorization header"""
        headers = {"Authorization": "InvalidFormat"}
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
    
    def test_missing_bearer_prefix(self, auth_token):
        """Test with missing 'Bearer' prefix"""
        headers = {"Authorization": auth_token}  # Missing "Bearer "
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
    
    def test_empty_authorization_header(self):
        """Test with empty authorization header"""
        headers = {"Authorization": ""}
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
    
    def test_token_with_invalid_signature(self, test_user):
        """Test token with invalid signature"""
        # Create token with wrong secret
        fake_token = jwt.encode(
            {"sub": test_user["username"], "exp": datetime.utcnow() + timedelta(hours=1)},
            "wrong_secret_key",
            algorithm=ALGORITHM
        )
        
        headers = {"Authorization": f"Bearer {fake_token}"}
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
    
    def test_token_missing_subject_claim(self):
        """Test token missing 'sub' claim"""
        # Create token without 'sub' claim
        token = jwt.encode(
            {"exp": datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
