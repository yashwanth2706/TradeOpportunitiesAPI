"""
Authentication Tests for Trade Opportunities API

Tests JWT authentication, user registration, login, and token validation.

Test Coverage:
- User registration (new user, duplicate, validation)
- User login (valid/invalid credentials)
- JWT token generation and validation
- Token expiration
- Password hashing and verification
- Protected endpoint access control
"""

import pytest
import time
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from jose import jwt

from app.config import settings
from app.core.auth import users_db
from app.core.security import hash_password, verify_password, create_access_token
from conftest import client

# Extract config values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


@pytest.mark.auth
class TestAuthentication:
    """Test authentication functionality"""
    
    def test_register_new_user(self):
        """Test registering a new user"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "newuser", "password": "newpass123"}
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "newuser" in users_db
    
    def test_register_duplicate_user(self, test_user):
        """Test registering a user that already exists"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": test_user["username"], "password": "anypass"}
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_short_username(self):
        """Test registration with username too short"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "ab", "password": "validpass123"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_register_short_password(self):
        """Test registration with password too short"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "validuser", "password": "short"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_login_valid_credentials(self, test_user):
        """Test login with valid credentials using /token endpoint"""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": test_user["username"], "password": test_user["password"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self):
        """Test login with non-existent username"""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "nonexistent", "password": "anypass"}
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_invalid_password(self, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": test_user["username"], "password": "wrongpass"}
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_token_endpoint_oauth2(self, test_user):
        """Test OAuth2 compatible token endpoint"""
        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_access_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without authentication"""
        response = client.get("/api/v1/analyze/technology")
        assert response.status_code == 401
        assert "not authenticated" in response.text.lower()
    
    def test_access_protected_endpoint_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
    
    def test_access_protected_endpoint_with_valid_token(
        self, auth_headers, mock_data_collector, mock_llm_client
    ):
        """Test accessing protected endpoint with valid token"""
        response = client.get("/api/v1/analyze/technology", headers=auth_headers)
        assert response.status_code == 200
    
    def test_jwt_token_contains_correct_claims(self, test_user):
        """Test that JWT token contains correct claims"""
        before_timestamp = time.time()
        
        response = client.post(
            "/api/v1/auth/token",
            data={"username": test_user["username"], "password": test_user["password"]}
        )
        
        after_timestamp = time.time()
        token = response.json()["access_token"]
        
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload["sub"] == test_user["username"]
        assert "exp" in payload
        
        # Check expiration is approximately ACCESS_TOKEN_EXPIRE_MINUTES from now
        exp_timestamp = payload["exp"]
        expected_exp_min = before_timestamp + (ACCESS_TOKEN_EXPIRE_MINUTES * 60) - 2  # Allow 2 second tolerance before
        expected_exp_max = after_timestamp + (ACCESS_TOKEN_EXPIRE_MINUTES * 60) + 2   # Allow 2 second tolerance after
        
        assert expected_exp_min <= exp_timestamp <= expected_exp_max
    
    def test_expired_token_rejected(self, test_user):
        """Test that expired tokens are rejected"""
        # Create a token that expired 1 hour ago
        expired_token = create_access_token(
            data={"sub": test_user["username"]},
            expires_delta=timedelta(minutes=-60)
        )
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/v1/analyze/technology", headers=headers)
        assert response.status_code == 401
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        # Hash should be different from original
        assert hashed != password
        
        # Verification should succeed with correct password
        assert verify_password(password, hashed) is True
        
        # Verification should fail with wrong password
        assert verify_password("wrongpassword", hashed) is False
