"""
Utility Tests for Trade Opportunities API

Tests helper functions and utilities.

Test Coverage:
- JWT token creation with default expiry
- JWT token creation with custom expiry
- Token payload validation
- Analysis report file saving with duplicate filename handling
"""

import pytest
import time
import os
from datetime import timedelta
from jose import jwt

from app.config import settings
from app.core.security import create_access_token
from app.services.llm_client import save_analysis_report

# Extract config values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


@pytest.mark.utilities
class TestUtilities:
    """Test utility functions"""
    
    def test_create_access_token_default_expiry(self):
        """Test creating access token with default expiry"""
        token = create_access_token(data={"sub": "testuser"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload["sub"] == "testuser"
        assert "exp" in payload
    
    def test_create_access_token_custom_expiry(self):
        """Test creating access token with custom expiry"""
        custom_delta = timedelta(minutes=30)
        before_timestamp = time.time()
        
        token = create_access_token(
            data={"sub": "testuser"},
            expires_delta=custom_delta
        )
        
        after_timestamp = time.time()
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Get the expiration timestamp from the token
        exp_timestamp = payload["exp"]
        
        # Calculate expected expiry range as timestamps (30 minutes from now)
        expected_exp_min = before_timestamp + (30 * 60) - 2  # Allow 2 second tolerance before
        expected_exp_max = after_timestamp + (30 * 60) + 2   # Allow 2 second tolerance after
        
        # Should be approximately 30 minutes from now (with some tolerance)
        assert expected_exp_min <= exp_timestamp <= expected_exp_max


@pytest.mark.utilities
class TestAnalysisReportSaving:
    """Test analysis report file saving functionality directly in reports directory"""
    
    def test_save_analysis_report_creates_incremented_filename_with_by_pattern(self):
        """Test that duplicate filenames create incremented versions with _by_ pattern"""
        # Get the actual reports directory where save_analysis_report saves files
        # This is TradeOpportunitiesAPI/reports (same level as tests/)
        test_dir = os.path.dirname(__file__)  # tests/
        project_root = os.path.dirname(test_dir)  # TradeOpportunitiesAPI/
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # Test filename pattern with _by_
        filename = "test_duplicate_sector_report_by_test-model.md"
        file_path_1 = os.path.join(reports_dir, filename)
        
        try:
            # Create first file
            content1 = "# Test Report 1"
            with open(file_path_1, 'w', encoding='utf-8') as f:
                f.write(content1)
            assert os.path.exists(file_path_1)
            
            # Save second report with same filename - should create incremented version
            content2 = "# Test Report 2"
            result_path_2 = save_analysis_report(content2, filename)
            
            assert os.path.exists(result_path_2)
            # Should have a counter in parentheses
            assert "(" in result_path_2 and ")" in result_path_2
            assert "_by_test-model.md" in result_path_2
            assert result_path_2 != file_path_1  # Must be different from original
            
            # Verify content
            with open(result_path_2, 'r', encoding='utf-8') as f:
                assert f.read() == content2
            
            # Save third report - should create another incremented version
            content3 = "# Test Report 3"
            result_path_3 = save_analysis_report(content3, filename)
            
            assert os.path.exists(result_path_3)
            assert "(" in result_path_3 and ")" in result_path_3
            assert "_by_test-model.md" in result_path_3
            assert result_path_3 != file_path_1  # Different from original
            assert result_path_3 != result_path_2  # Different from second
            
            # Verify all files exist
            assert os.path.exists(file_path_1)
            assert os.path.exists(result_path_2)
            assert os.path.exists(result_path_3)
            
        finally:
            # Cleanup test files - remove all test_duplicate files
            for file in os.listdir(reports_dir):
                if file.startswith("test_duplicate_sector_report_") and file.endswith("_by_test-model.md"):
                    os.remove(os.path.join(reports_dir, file))
    
    def test_save_analysis_report_creates_incremented_filename_without_by_pattern(self):
        """Test duplicate filenames without _by_ pattern use fallback counter"""
        # Get the actual reports directory
        test_dir = os.path.dirname(__file__)  # tests/
        project_root = os.path.dirname(test_dir)  # TradeOpportunitiesAPI/
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        filename = "test_simple_duplicate.md"
        file_path_1 = os.path.join(reports_dir, filename)
        
        try:
            # Create first file
            content1 = "# Simple Report 1"
            with open(file_path_1, 'w', encoding='utf-8') as f:
                f.write(content1)
            
            # Save second report - should create incremented version
            content2 = "# Simple Report 2"
            result_path_2 = save_analysis_report(content2, filename)
            
            assert os.path.exists(result_path_2)
            # Should have a counter in parentheses
            assert "(" in result_path_2 and ")" in result_path_2
            assert "test_simple_duplicate_" in result_path_2
            assert ".md" in result_path_2
            assert result_path_2 != file_path_1  # Must be different from original
            
            # Verify content
            with open(result_path_2, 'r', encoding='utf-8') as f:
                assert f.read() == content2
            
            # Verify both files exist
            assert os.path.exists(file_path_1)
            assert os.path.exists(result_path_2)
            
        finally:
            # Cleanup - remove all test_simple_duplicate files
            for file in os.listdir(reports_dir):
                if file.startswith("test_simple_duplicate_") and file.endswith(".md"):
                    os.remove(os.path.join(reports_dir, file))
    
    def test_save_analysis_report_preserves_original_content(self):
        """Test that original file content is preserved when duplicate is created"""
        # Get the actual reports directory
        test_dir = os.path.dirname(__file__)  # tests/
        project_root = os.path.dirname(test_dir)  # TradeOpportunitiesAPI/
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        filename = "test_preserve_original_by_model.md"
        file_path_1 = os.path.join(reports_dir, filename)
        
        try:
            # Create original file
            original_content = "# Original Report\n\nThis is the original content."
            with open(file_path_1, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Create duplicate with different content
            duplicate_content = "# Duplicate Report\n\nThis is the duplicate content."
            result_path_2 = save_analysis_report(duplicate_content, filename)
            
            # Verify original file still has original content
            with open(file_path_1, 'r', encoding='utf-8') as f:
                assert f.read() == original_content
            
            # Verify duplicate file has new content
            with open(result_path_2, 'r', encoding='utf-8') as f:
                assert f.read() == duplicate_content
            
        finally:
            # Cleanup - remove all test_preserve_original files
            for file in os.listdir(reports_dir):
                if file.startswith("test_preserve_original_") and file.endswith("_by_model.md"):
                    os.remove(os.path.join(reports_dir, file))
