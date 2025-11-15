"""
Input Validation Tests for Trade Opportunities API

Tests Pydantic model validation for all inputs.

Test Coverage:
- Sector name validation (length, characters, format)
- Username validation (length constraints)
- Password validation (length constraints)
- Missing required fields
- Empty payloads
"""

import pytest
from fastapi.testclient import TestClient

from conftest import client


@pytest.mark.validation
class TestInputValidation:
    """Test input validation for various endpoints"""
    
    def test_sector_validation_too_short(self, auth_headers):
        """Test sector name validation - too short"""
        response = client.get("/api/v1/analyze/a", headers=auth_headers)
        assert response.status_code == 400
        assert "2 characters" in response.json()["detail"].lower() or "string_too_short" in response.json()["detail"].lower()
    
    def test_sector_validation_too_long(self, auth_headers):
        """Test sector name validation - too long"""
        long_sector = "a" * 31  # 31 characters
        response = client.get(f"/api/v1/analyze/{long_sector}", headers=auth_headers)
        assert response.status_code == 400
    
    def test_sector_validation_special_characters(self, auth_headers):
        """Test sector name validation - special characters"""
        invalid_sectors = ["+", "tech@sector", "123", "sect0r", "tech-nology"]
        
        for sector in invalid_sectors:
            response = client.get(f"/api/v1/analyze/{sector}", headers=auth_headers)
            assert response.status_code == 400, f"Sector '{sector}' should be rejected"
            assert "alphabetic" in response.json()["detail"].lower()
    
    def test_sector_validation_valid_names(
        self, auth_headers, mock_data_collector, mock_llm_client
    ):
        """Test sector name validation - valid names"""
        valid_sectors = [
            "technology",
            "pharmaceuticals",
            "agriculture",
            "dairy",
            "IT",
            "Pharmaceuticals"  # Mixed case should work
        ]
        
        for sector in valid_sectors:
            response = client.get(f"/api/v1/analyze/{sector}", headers=auth_headers)
            # Should not fail validation (might fail rate limit after 5 requests)
            assert response.status_code in [200, 429], \
                f"Sector '{sector}' should be valid"
    
    def test_username_validation_too_short(self):
        """Test username validation - too short"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "ab", "password": "validpass123"}
        )
        assert response.status_code == 422
    
    def test_username_validation_too_long(self):
        """Test username validation - too long"""
        long_username = "a" * 51  # 51 characters
        response = client.post(
            "/api/v1/auth/register",
            json={"username": long_username, "password": "validpass123"}
        )
        assert response.status_code == 422
    
    def test_password_validation_too_short(self):
        """Test password validation - too short"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "validuser", "password": "short"}
        )
        assert response.status_code == 422
    
    def test_password_validation_too_long(self):
        """Test password validation - too long"""
        long_password = "a" * 101  # 101 characters
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "validuser", "password": long_password}
        )
        assert response.status_code == 422
    
    def test_missing_username_in_registration(self):
        """Test registration with missing username"""
        response = client.post(
            "/api/v1/auth/register",
            json={"password": "validpass123"}
        )
        assert response.status_code == 422
    
    def test_missing_password_in_registration(self):
        """Test registration with missing password"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "validuser"}
        )
        assert response.status_code == 422
    
    def test_empty_json_in_registration(self):
        """Test registration with empty JSON"""
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422
    
    def test_sector_validation_empty_string(self, auth_headers):
        """Test sector name validation - empty string"""
        response = client.get("/api/v1/analyze/", headers=auth_headers)
        # Should get 404 (no route match) or 400 (validation error)
        assert response.status_code in [404, 400]
    
    def test_sector_validation_whitespace_only(self, auth_headers):
        """Test sector name validation - whitespace only"""
        response = client.get("/api/v1/analyze/   ", headers=auth_headers)
        assert response.status_code == 400
    
    def test_sector_validation_mixed_valid_invalid(self, auth_headers):
        """Test sector name validation - mixed valid and invalid characters"""
        invalid_sectors = ["tech123", "sector_name", "sector.name", "sector name"]
        
        for sector in invalid_sectors:
            response = client.get(f"/api/v1/analyze/{sector}", headers=auth_headers)
            assert response.status_code == 400, \
                f"Sector '{sector}' with mixed characters should be rejected"
