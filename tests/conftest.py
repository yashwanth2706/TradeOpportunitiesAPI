"""
Shared pytest fixtures for Trade Opportunities API test suite

This module contains all fixtures that are shared across multiple test modules.
Fixtures include:
- Test data cleanup (autouse)
- Test user creation
- Authentication tokens and headers
- Mock objects for external services
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Import the app and utilities from new structure
from app.main import create_app
from app.core.auth import users_db
from app.core.session import session_manager
from app.core.security import hash_password

# Create app instance and test client
app = create_app()
client = TestClient(app)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def clear_test_data():
    """Clear in-memory storage before and after each test"""
    users_db.clear()
    session_manager._sessions.clear()
    yield
    users_db.clear()
    session_manager._sessions.clear()


@pytest.fixture
def test_user():
    """Create a test user and return credentials"""
    username = "testuser"
    password = "testpass123"
    users_db[username] = hash_password(password)
    return {"username": username, "password": password}


@pytest.fixture
def auth_token(test_user):
    """Register a user and return a valid JWT token"""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user["username"], "password": test_user["password"]}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Return authorization headers with valid token"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def mock_data_collector():
    """Mock the data collector to avoid external API calls"""
    with patch('app.api.v1.endpoints.analysis.data_collector.search_news', new_callable=AsyncMock) as mock:
        mock.return_value = [
            {
                "title": "Test Article 1",
                "snippet": "Test snippet 1",
                "link": "https://example.com/1"
            },
            {
                "title": "Test Article 2", 
                "snippet": "Test snippet 2",
                "link": "https://example.com/2"
            }
        ]
        yield mock


@pytest.fixture
def mock_llm_client():
    """Mock the LLM client to avoid external API calls"""
    with patch('app.api.v1.endpoints.analysis.llm_client.analyze', new_callable=AsyncMock) as mock:
        mock.return_value = "# Test Report\n\nThis is a test market analysis report."
        yield mock
