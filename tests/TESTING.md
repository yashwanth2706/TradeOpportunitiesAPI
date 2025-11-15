# Test Suite Documentation

## Overview

This document describes the comprehensive test suite for the Trade Opportunities API. The test suite uses pytest and covers authentication, rate limiting, session expiry, and input validation.

## Test Structure

The test suite is organized into **7 separate modules** for better maintainability:

```
tests/
├── conftest.py                  # Shared fixtures and test client
├── test_authentication.py       # Authentication & JWT tests (15 tests)
├── test_rate_limiting.py        # Rate limiting (token bucket) tests (7 tests)
├── test_session_expiry.py       # Session management tests (5 tests)
├── test_input_validation.py     # Input validation tests (14 tests)
├── test_integration.py          # End-to-end integration tests (4 tests)
├── test_utilities.py            # Utility function tests (2 tests)
├── test_edge_cases.py           # Edge cases & error handling (5 tests)
├── pytest.ini                   # Pytest configuration
└── TESTING.md                   # This documentation
```

**Benefits of Modular Structure:**
- ✅ Better organization and discoverability
- ✅ Faster test runs (run only relevant modules)
- ✅ Easier maintenance and debugging
- ✅ Clearer test ownership and categorization
- ✅ Shared fixtures in `conftest.py` (DRY principle)

## Running Tests

### Quick Start

```bash
# Run all tests
pytest tests/ -v

# Run all tests with summary
pytest tests/

# Run specific test module
pytest tests/test_authentication.py -v
```

### Specific Test Modules

```bash
# Authentication tests only (15 tests)
pytest tests/test_authentication.py -v

# Rate limiting tests only (7 tests)
pytest tests/test_rate_limiting.py -v

# Session expiry tests only (5 tests)
pytest tests/test_session_expiry.py -v

# Input validation tests only (14 tests)
pytest tests/test_input_validation.py -v

# Integration tests only (4 tests)
pytest tests/test_integration.py -v

# Utility tests only (2 tests)
pytest tests/test_utilities.py -v

# Edge cases only (5 tests)
pytest tests/test_edge_cases.py -v
```

### Advanced Options

```bash
# Generate coverage report
pytest tests/ --cov=app --cov-report=html

# Run until first failure
pytest tests/ -x

# Verbose output with print statements
pytest tests/ -v -s

# Re-run only failed tests
pytest tests/ --lf

# Run specific test by name
pytest tests/test_authentication.py::TestAuthentication::test_login_valid_credentials -v

# Run all tests matching a keyword
pytest tests/ -k "login" -v
pytest tests/ -k "rate_limit" -v
```

### Using pytest directly

```bash
# Run with markers (tags)
pytest tests/ -m auth          # Auth tests
pytest tests/ -m ratelimit     # Rate limit tests
pytest tests/ -m session       # Session tests
pytest tests/ -m validation    # Validation tests
pytest tests/ -m integration   # Integration tests
pytest tests/ -m utilities     # Utility tests
pytest tests/ -m edge          # Edge case tests

# Run specific test class
pytest tests/test_authentication.py::TestAuthentication -v

# Run specific test method
pytest tests/test_authentication.py::TestAuthentication::test_login_valid_credentials -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x

# Run last failed tests only
pytest tests/ --lf

# Run tests matching keyword
pytest tests/ -k "login"
pytest tests/ -k "not slow"

# Run multiple modules
pytest tests/test_authentication.py tests/test_rate_limiting.py -v
```

## Test Categories

### 1. Authentication Tests (15 tests)

**Module:** `test_authentication.py`

Tests JWT authentication, user registration, login, and token validation.

**Key Tests:**
- ✅ `test_register_new_user` - User registration flow
- ✅ `test_register_duplicate_user` - Prevent duplicate usernames
- ✅ `test_login_valid_credentials` - Login with correct credentials
- ✅ `test_login_invalid_username` - Login with wrong username
- ✅ `test_login_invalid_password` - Login with wrong password
- ✅ `test_access_protected_endpoint_without_token` - Require auth
- ✅ `test_access_protected_endpoint_with_invalid_token` - Invalid token
- ✅ `test_jwt_token_contains_correct_claims` - JWT structure validation
- ✅ `test_expired_token_rejected` - Token expiration enforcement
- ✅ `test_password_hashing` - Password hashing security

**Example:**
```bash
pytest tests/test_authentication.py -v
pytest tests/test_authentication.py::TestAuthentication::test_login_valid_credentials -v
```

### 2. Rate Limiting Tests (7 tests)

**Module:** `test_rate_limiting.py`

Tests the token bucket rate limiting algorithm.

**Key Tests:**
- ✅ `test_rate_limit_allows_initial_requests` - Allow requests within limit
- ✅ `test_rate_limit_blocks_excess_requests` - Block after limit exceeded
- ✅ `test_rate_limit_per_user` - Separate limits per user
- ✅ `test_rate_limit_token_bucket_refill` - Token bucket refill mechanism
- ✅ `test_rate_limit_partial_refill` - Partial time passage handling
- ✅ `test_session_info_usage_count` - Usage tracking

**Example:**
```bash
pytest tests/test_rate_limiting.py -v
pytest tests/ -m ratelimit -v
```

### 3. Session Expiry Tests (5 tests)

**Module:** `test_session_expiry.py`

Tests session lifecycle and expiration handling.

**Key Tests:**
- ✅ `test_session_is_not_expired_initially` - New sessions valid
- ✅ `test_session_expires_after_timeout` - Expiration after timeout
- ✅ `test_session_not_expired_before_timeout` - Valid before timeout
- ✅ `test_expired_session_requires_relogin` - Expired sessions require re-login
- ✅ `test_session_capacity_and_tokens_initialized` - Correct initialization

**Example:**
```bash
pytest tests/test_session_expiry.py -v
pytest tests/ -m session -v
```

### 4. Input Validation Tests (14 tests)

**Module:** `test_input_validation.py`

Tests Pydantic model validation for all inputs.

**Key Tests:**
- ✅ `test_sector_validation_too_short` - Sector < 2 chars rejected
- ✅ `test_sector_validation_too_long` - Sector > 30 chars rejected
- ✅ `test_sector_validation_special_characters` - Non-alpha rejected
- ✅ `test_sector_validation_valid_names` - Valid sectors accepted
- ✅ `test_username_validation_too_short` - Username < 3 chars rejected
- ✅ `test_password_validation_too_short` - Password < 6 chars rejected
- ✅ `test_missing_username_in_registration` - Required field validation
- ✅ `test_empty_json_in_registration` - Empty payload rejected

**Example:**
```bash
pytest tests/test_input_validation.py -v
pytest tests/ -m validation -v
```

### 5. Integration Tests (4 tests)

**Module:** `test_integration.py`

End-to-end tests combining multiple features.

**Key Tests:**
- ✅ `test_complete_user_flow` - Register → Login → Analyze workflow
- ✅ `test_rate_limit_with_session_expiry` - Combined rate limit & session
- ✅ `test_health_endpoint_shows_session_count` - Health monitoring
- ✅ `test_multiple_users_concurrent_access` - Concurrent user access

**Example:**
```bash
pytest tests/test_integration.py -v
pytest tests/ -m integration -v
```

### 6. Utility Tests (2 tests)

**Module:** `test_utilities.py`

Tests helper functions.

**Key Tests:**
- ✅ `test_create_access_token_default_expiry` - Token creation
- ✅ `test_create_access_token_custom_expiry` - Custom expiration

**Example:**
```bash
pytest tests/test_utilities.py -v
pytest tests/ -m utilities -v
```

### 7. Edge Cases Tests (5 tests)

**Module:** `test_edge_cases.py`

Tests error handling and edge cases.

**Key Tests:**
- ✅ `test_malformed_authorization_header` - Malformed headers
- ✅ `test_missing_bearer_prefix` - Missing "Bearer" prefix
- ✅ `test_token_with_invalid_signature` - Invalid JWT signature
- ✅ `test_token_missing_subject_claim` - Missing required claims
- ✅ `test_empty_authorization_header` - Empty header handling

**Example:**
```bash
pytest tests/test_edge_cases.py -v
pytest tests/ -m edge -v
```

## Test Fixtures

All fixtures are centralized in `conftest.py` and automatically available to all test modules.

### Available Fixtures

```python
@pytest.fixture(autouse=True)
def clear_test_data():
    """Automatically clears users and sessions before/after each test"""
    
@pytest.fixture
def test_user():
    """Creates a test user and returns credentials"""
    # Returns: {"username": "testuser", "password": "testpass123"}
    
@pytest.fixture
def auth_token(test_user):
    """Returns a valid JWT token for the test user"""
    
@pytest.fixture
def auth_headers(auth_token):
    """Returns authorization headers with valid token"""
    # Returns: {"Authorization": "Bearer <token>"}
    
@pytest.fixture
def mock_data_collector():
    """Mocks the data collector to avoid external API calls"""
    
@pytest.fixture
def mock_llm_client():
    """Mocks the LLM client to avoid external API calls"""
```

**Note:** The `client` object (TestClient) is also defined in `conftest.py` and imported by all test modules.

### Using Fixtures

```python
def test_example(test_user, auth_token, auth_headers):
    # test_user contains credentials
    username = test_user["username"]
    
    # auth_token is a valid JWT token
    assert len(auth_token) > 0
    
    # auth_headers can be used directly with client
    response = client.get("/analyze/tech", headers=auth_headers)
```

## Mock Objects

Tests use mocks to avoid external API dependencies:

```python
# Mocked data collector returns fake news snippets
mock_data_collector.return_value = [
    {"title": "Article 1", "snippet": "...", "link": "..."},
    {"title": "Article 2", "snippet": "...", "link": "..."}
]

# Mocked LLM client returns test report
mock_llm_client.return_value = "# Test Report\n\nAnalysis..."
```

This ensures tests:
- Run quickly without network calls
- Are deterministic and repeatable
- Don't consume API quotas
- Work offline

## Coverage

Generate coverage reports:

```bash
# HTML coverage report
pytest tests/ --cov=app --cov-report=html
# View: htmlcov/index.html

# Terminal coverage report
pytest tests/ --cov=app --cov-report=term

# Coverage with missing lines
pytest tests/ --cov=app --cov-report=term-missing

# Coverage for specific module
pytest tests/test_authentication.py --cov=app.core.auth --cov-report=term
```

**Target Coverage:** 80%+ (configured in pytest.ini)

## Test Output Examples

### Successful Test Run
```
================================================== test session starts ==================================================
tests/test_authentication.py::TestAuthentication::test_register_new_user PASSED                              [  2%]
tests/test_authentication.py::TestAuthentication::test_login_valid_credentials PASSED                        [  4%]
tests/test_rate_limiting.py::TestRateLimiting::test_rate_limit_blocks_excess_requests PASSED                 [  6%]
tests/test_integration.py::TestIntegration::test_complete_user_flow PASSED                                   [ 10%]
...
================================================== 52 passed in 2.34s ===================================================
```

### Failed Test
```
================================================== FAILURES =============================================================
_______________________________ TestAuthentication.test_login_invalid_password __________________________________________

    def test_login_invalid_password(self, test_user):
        response = client.post("/token", data={"username": test_user["username"], "password": "wrongpass"})
>       assert response.status_code == 401
E       assert 200 == 401

tests/test_authentication.py:142: AssertionError
```

### Coverage Report
```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
app/core/auth.py                  45      2    96%   67-68
app/core/security.py              30      1    97%   42
app/core/rate_limit.py            35      3    91%   45-47
app/api/v1/endpoints/auth.py      40      2    95%   58-59
app/services/llm_client.py        80      8    90%   45-48, 67-70
------------------------------------------------------------
TOTAL                            355     25    93%
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest test_main.py -v --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### GitLab CI Example

```yaml
test:
  image: python:3.9
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest test_main.py -v --cov=. --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

## Troubleshooting

### Tests Fail with "SECRET_KEY not set"

**Solution:** Create `.env` file with SECRET_KEY:
```bash
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > .env
```

### Import Errors

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Tests Timeout

**Solution:** Mocks may not be working. Check that fixtures are applied:
```python
def test_example(mock_data_collector, mock_llm_client):
    # Both fixtures must be in function signature
    pass
```

### Rate Limit Tests Fail

**Solution:** Clear sessions between tests (should happen automatically with `clear_test_data` fixture)

### Session Expiry Tests Fail

**Solution:** Check system time is correct. Tests rely on `datetime.utcnow()`.

## Best Practices

### Writing New Tests

1. **Use descriptive names:**
   ```python
   def test_rate_limit_allows_requests_within_capacity():  # Good
   def test_rl():  # Bad
   ```

2. **Test one thing per test:**
   ```python
   def test_login_with_valid_credentials():  # Good - one assertion
       assert response.status_code == 200
   
   def test_login():  # Bad - multiple unrelated checks
       assert response.status_code == 200
       assert rate_limit_not_exceeded
       assert session_created
   ```

3. **Use fixtures for setup:**
   ```python
   def test_protected_endpoint(auth_headers):  # Good - uses fixture
       response = client.get("/analyze/tech", headers=auth_headers)
   ```

4. **Mock external dependencies:**
   ```python
   def test_analysis(mock_data_collector, mock_llm_client):  # Good
       # Test won't make real API calls
   ```

5. **Assert on specific values:**
   ```python
   assert response.status_code == 401  # Good - specific
   assert response.status_code != 200  # Bad - vague
   ```

### Test Organization

- Group related tests in classes
- Use fixtures for common setup
- Keep tests independent (no shared state)
- Test both success and failure cases
- Include edge cases

## Performance

### Typical Test Execution Times

- **All tests:** ~2-3 seconds
- **Authentication tests:** ~0.5 seconds
- **Rate limiting tests:** ~0.8 seconds
- **Session expiry tests:** ~0.3 seconds
- **Input validation tests:** ~0.4 seconds

Tests are fast because:
- No real API calls (mocked)
- In-memory storage
- No database operations
- Minimal I/O

## Maintenance

### When to Update Tests

- ✅ New feature added → Add new tests
- ✅ Bug fixed → Add regression test
- ✅ API changes → Update affected tests
- ✅ Requirements change → Update validation tests
- ✅ Security update → Add security tests

### Regular Checks

```bash
# Weekly: Full test suite with coverage
./run_tests.sh coverage

# Before commit: Quick test run
./run_tests.sh quick

# After changes: Affected tests only
pytest test_main.py -k "rate_limit" -v
```

## Additional Resources

- **pytest documentation:** https://docs.pytest.org/
- **FastAPI testing:** https://fastapi.tiangolo.com/tutorial/testing/
- **Coverage.py:** https://coverage.readthedocs.io/

## Summary

✅ **52 comprehensive tests** organized into 7 modular files  
✅ **Easy to run** with `pytest tests/`  
✅ **Fast execution** (~2-3 seconds)  
✅ **Modular structure** for better organization and maintenance  
✅ **Shared fixtures** in `conftest.py` (DRY principle)  
✅ **High coverage** target (80%+)  
✅ **Well documented** with clear examples  
✅ **CI/CD ready** for automated testing  
✅ **Mocked externals** for reliability  
✅ **Independent tests** for isolation  
✅ **Pytest markers** for selective test execution

**Quick Reference:**
```bash
# Run all tests
pytest tests/ -v

# Run specific module
pytest tests/test_authentication.py -v

# Run by marker
pytest tests/ -m auth -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

Run tests regularly to ensure API quality and catch regressions early!
