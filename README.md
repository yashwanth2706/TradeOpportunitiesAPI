# Trade Opportunities API

A production-ready FastAPI application for analyzing trade opportunities across different sectors using AI-powered market analysis.

## Project Structure

```
TradeOpportunitiesAPI/
├── app/                          # Main application package
│   ├── api/                      # API routes
│   │   └── v1/                   # API version 1
│   │       ├── endpoints/        # Individual endpoint modules
│   │       │   ├── auth.py       # Authentication endpoints
│   │       │   ├── analysis.py   # Analysis endpoints
│   │       │   └── health.py     # Health check endpoints
│   │       └── router.py         # Main API router
│   │
│   ├── core/                     # Core functionality
│   │   ├── auth.py               # Authentication logic
│   │   ├── security.py           # Password hashing, JWT tokens
│   │   ├── rate_limit.py         # Rate limiting (token bucket)
│   │   └── session.py            # Session management
│   │
│   ├── models/                   # Pydantic models
│   │   ├── auth.py               # Authentication models
│   │   └── analysis.py           # Analysis models
│   │
│   ├── services/                 # Business logic services
│   │   ├── data_collector.py     # Data collection service
│   │   └── llm_client.py         # LLM integration service
│   │
│   ├── db/                       # Database (for future use)
│   │
│   ├── config.py                 # Application configuration
│   ├── dependencies.py           # Shared FastAPI dependencies
│   └── main.py                   # FastAPI app initialization
│
├── tests/                        # Test suite
├── reports/                      # Generated analysis reports
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
└── README.md                     # This file
```

## Quick Start

### Prerequisites

- **Python 3.9+** (3.11+ recommended)
- **pip** package manager
- **Git** (for cloning the repository)
- **Gemini API Key** (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/yashwanth2706/TradeOpportunitiesAPI.git
cd TradeOpportunitiesAPI
```
### (Recommended Fastest way to setup environment) Run setup.py and run.py
- If Windows
```bash
python setup.py
```
- If Linux/MacOS
```bash
python3 setup.py
```
- This will create virtual environment and install dependencies from requirements.txt
- Automatically deactivates once done
- Please activate virtual envirornment manually again, See Step 2 for the commands
- Creates .env file if doesnot exists, securely generates secretkey and adds it
- Manual configuration still needed for other variables inside .env like API_KEY, MODEL_NAME, DEBUG...etc 
- Manually activate the virtual envirornment from below commands depending upon your system
- Once .env configured, virtual envirornment activated run: run.py
- If Windows
```bash
python run.py
```
- If Linux/MacOS
```bash
python3 run.py
```

### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Expected packages:**
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `python-jose[cryptography]` - JWT tokens
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data parsing
- `google-genai` - Google Gemini AI SDK
- `duckduckgo-search` - Web search
- `pytest`, `pytest-asyncio`, `pytest-cov` - Testing
- `ruff` - Linting

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example (if available)
cp .env.example .env

# Or create manually
touch .env
```

**Required environment variables:**

```env
# Security (REQUIRED)
SECRET_KEY=your-secret-key-here-minimum-32-characters

# Gemini AI (REQUIRED)
GEMINI_API_KEY=your-gemini-api-key-from-google
LLM_MODEL_NAME=gemini-2.0-flash-exp

# Authentication (OPTIONAL - defaults shown)
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Rate Limiting (OPTIONAL - defaults shown)
RATE_LIMIT_CAPACITY=5
RATE_LIMIT_REFILL_SECONDS=60

# Application (OPTIONAL - defaults shown)
LOG_LEVEL=INFO
DEBUG=False
```

**Generate a secure SECRET_KEY:**

```bash
# Python one-liner
python -c "import secrets; print(secrets.token_hex(32))"

# Or use openssl
openssl rand -hex 32
```

### 5. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.9+

# Check installed packages
pip list

# Run linter to verify code quality
ruff check app/ tests/
```

### 6. Run Tests (Optional but Recommended)

```bash
# Run all tests
pytest tests/ -v

# Should see: 53 passed in ~20-25s
```

### 7. Run the Application

**Option 1: Using run.py (Recommended)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
**Option 3: Directly Run with Python**
```bash
python -m uvicorn app.main:app --reload
```

### 8. Verify Application is Running

**Check the startup logs:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Test the endpoints:**

1. **Health Check:**
   ```bash
   curl http://localhost:8000/api/v1/health
   # Expected: {"status":"ok","active_sessions":0}
   ```

2. **API Documentation:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

3. **Root Endpoint:**
   ```bash
   curl http://localhost:8000/api/v1/
   # Expected: {"message":"Trade Opportunities API","docs":"/docs","version":"0.1.0"}
   ```

### 9. Create Your First User

**Using Swagger UI (http://localhost:8000/docs):**
1. Navigate to `POST /api/v1/auth/register`
2. Click "Try it out"
3. Enter username and password
4. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### 10. Get Authentication Token

**Using Swagger UI:**
1. Navigate to `POST /api/v1/auth/token`
2. Click "Try it out"
3. Enter your credentials
4. Click "Execute"
5. Copy the `access_token` from the response

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

### 11. Make Your First Analysis Request

```bash
curl -X GET "http://localhost:8000/api/v1/analyze/technology" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "sector": "technology",
  "report_markdown": "# Technology Sector Analysis\n\n...",
  "generated_at": "2025-11-15T10:30:00Z",
  "model_used": "gemini-2.0-flash-exp"
}
```

The analysis report will also be saved in the `reports/` directory.

## 📚 API Documentation

### Authentication

All endpoints require JWT authentication except for registration and login.

#### Register a New User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

#### Login
```http
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

### Analysis

#### Analyze a Sector
```http
GET /api/v1/analyze/{sector}
Authorization: Bearer <your_token>
```

Example:
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/analyze/technology
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with automatic salt generation
- **Rate Limiting**: 5 requests per minute per user (token bucket algorithm)
- **Session Management**: Automatic session expiration
- **Input Validation**: Pydantic models for request validation

## 🧪 Testing

### Test Suite Overview

The project includes **53 comprehensive tests** organized into 7 modules:

```
tests/
├── conftest.py                    # Shared fixtures and test configuration
├── pytest.ini                     # Pytest configuration
├── test_authentication.py         # Authentication & JWT tests (14 tests)
├── test_rate_limiting.py          # Rate limiting tests (7 tests)
├── test_session_expiry.py         # Session management tests (5 tests)
├── test_input_validation.py       # Input validation tests (14 tests)
├── test_integration.py            # End-to-end integration tests (4 tests)
├── test_utilities.py              # Utility function tests (5 tests)
├── test_edge_cases.py             # Edge cases & error handling (5 tests)
└── TESTING.md                     # Detailed testing documentation
```

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
# Expected: 53 passed in ~20-25s
```

**Run specific test module:**
```bash
pytest tests/test_authentication.py -v
pytest tests/test_rate_limiting.py -v
pytest tests/test_integration.py -v
```

**Run tests by category (using markers):**
```bash
pytest tests/ -m auth          # Authentication tests
pytest tests/ -m ratelimit     # Rate limiting tests
pytest tests/ -m session       # Session tests
pytest tests/ -m validation    # Input validation tests
pytest tests/ -m integration   # Integration tests
pytest tests/ -m utilities     # Utility tests
pytest tests/ -m edge          # Edge case tests
```

**Run with coverage report:**
```bash
# Terminal coverage report
pytest tests/ --cov=app --cov-report=term

# HTML coverage report (opens in browser)
pytest tests/ --cov=app --cov-report=html
# View: htmlcov/index.html
```

**Run specific test:**
```bash
pytest tests/test_authentication.py::TestAuthentication::test_login_valid_credentials -v
```

**Run with verbose output and short traceback:**
```bash
pytest tests/ -v --tb=short
```

**Run tests in parallel (faster):**
```bash
pip install pytest-xdist
pytest tests/ -n auto
```

### Test Coverage

Target: **80%+** code coverage

Check coverage:
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Development Workflow

1. **Before making changes:**
   ```bash
   # Run tests to ensure baseline
   pytest tests/ -v
   ```

2. **After making changes:**
   ```bash
   # Run tests again
   pytest tests/ -v
   
   # Run linter
   ruff check app/ tests/
   
   # Fix linting issues automatically
   ruff check --fix app/ tests/
   ```

3. **Before committing:**
   ```bash
   # Run full test suite with coverage
   pytest tests/ --cov=app --cov-report=html
   
   # Verify no linting errors
   ruff check app/ tests/
   ```

### Writing New Tests

See `tests/TESTING.md` for detailed testing guidelines and examples.

**Test template:**
```python
import pytest
from fastapi.testclient import TestClient
from conftest import client

@pytest.mark.your_category
class TestYourFeature:
    """Test your feature description"""
    
    def test_your_scenario(self, auth_headers):
        """Test that your scenario works correctly"""
        response = client.get("/api/v1/endpoint", headers=auth_headers)
        assert response.status_code == 200
        assert "expected_key" in response.json()
```

## 🏭 Production Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using systemd

Create `/etc/systemd/system/trade-api.service`:

```ini
[Unit]
Description=Trade Opportunities API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/TradeOpportunitiesAPI
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📊 Architecture Decisions

### Why This Structure?

1. **Separation of Concerns**: Each module has a single responsibility
2. **Scalability**: Easy to add new versions, endpoints, or services
3. **Testability**: Isolated components are easier to test
4. **Maintainability**: Clear organization makes code easy to navigate
5. **Best Practices**: Follows FastAPI and Python standards

### Key Design Patterns

- **Dependency Injection**: Used for auth and shared dependencies
- **Repository Pattern**: Services encapsulate business logic
- **Factory Pattern**: App creation in main.py
- **Token Bucket**: Rate limiting algorithm
- **Session Management**: Automatic expiration and cleanup of user sessions
- **Input Validation**: Pydantic models ensure type safety and data integrity

## 🔧 Configuration

All configuration is centralized in `app/config.py`:

- Application settings
- Security parameters
- Rate limiting configuration
- API keys
- Logging levels

## 📝 API Versioning

The API uses URL path versioning:
- Current: `/api/v1/...`
- Future: `/api/v2/...` (when needed)

This allows gradual migration and backward compatibility.

## 🐛 Troubleshooting

### Setup Issues

#### Virtual Environment Not Activating (Windows)

**Problem:** PowerShell execution policy prevents script execution

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Module Not Found Errors

**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
# Make sure you're in the correct directory
cd TradeOpportunitiesAPI

# Verify virtual environment is activated
# Windows: (.venv) should appear in prompt
# Linux/Mac: (.venv) should appear in prompt

# Reinstall dependencies
pip install -r requirements.txt
```

#### SECRET_KEY Error on Startup

**Problem:** `SECRET_KEY is not configured`

**Solution:**
```bash
# Generate a new secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Add to .env file
echo "SECRET_KEY=<generated-key>" >> .env
```

### Runtime Issues

#### 1. Import Errors

**Problem:** `ImportError` or `ModuleNotFoundError`

**Solution:**
- Ensure you're running from the project root (`TradeOpportunitiesAPI/TradeOpportunitiesAPI/`)
- Activate virtual environment: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (Linux/Mac)
- Reinstall dependencies: `pip install -r requirements.txt`

#### 2. Authentication Fails

**Problem:** `401 Unauthorized` or invalid token errors

**Solutions:**
- Verify SECRET_KEY is set in `.env`
- Ensure SECRET_KEY is at least 32 characters
- Check token hasn't expired (default: 30 minutes)
- Verify you're sending token in header: `Authorization: Bearer <token>`

#### 3. Rate Limit Hit

**Problem:** `429 Too Many Requests`

**Solutions:**
- Default: 5 requests per 60 seconds per user
- Wait for token bucket to refill (check `Retry-After` header)
- Adjust rate limits in `.env`:
  ```env
  RATE_LIMIT_CAPACITY=10
  RATE_LIMIT_REFILL_SECONDS=60
  ```

#### 4. LLM/Gemini API Fails

**Problem:** `Unable to perform analysis` or Gemini API errors

**Solutions:**
- Verify `GEMINI_API_KEY` is set correctly in `.env`
- Check API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Verify model name is correct (default: `gemini-2.0-flash-exp`)
- Check API quotas and usage limits
- Verify internet connectivity

#### 5. Session Expired

**Problem:** `401 Unauthorized - session expired`

**Solutions:**
- Sessions expire after 30 minutes by default
- Get a new token using `/api/v1/auth/token`
- Adjust session timeout in `.env`:
  ```env
  ACCESS_TOKEN_EXPIRE_MINUTES=60
  ```

#### 6. Port Already in Use

**Problem:** `Error: [Errno 48] Address already in use`

**Solutions:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac:
lsof -i :8000
kill -9 <process_id>

# Or use a different port
uvicorn app.main:app --port 8001
```

#### 7. Test Failures

**Problem:** Tests failing after setup

**Solutions:**
```bash
# Clear pytest cache
pytest --cache-clear

# Run with verbose output
pytest tests/ -v --tb=short

# Check specific test file
pytest tests/test_authentication.py -v

# Verify all dependencies installed
pip install -r requirements.txt
```

### Debug Mode

Enable detailed logging for troubleshooting:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

**View logs:**
```bash
# Logs will show detailed information
python run.py

# Look for:
# - Environment variable loading
# - Database connections
# - API request/response details
# - Error stack traces
```

### Getting Help

1. **Check logs**: Look for error messages in console output
2. **Run tests**: `pytest tests/ -v` to verify system health
3. **Check documentation**: Review this README and API docs at `/docs`
4. **Verify environment**: Ensure all `.env` variables are set correctly
5. **Update dependencies**: `pip install --upgrade -r requirements.txt`

## 📚 Additional Resources

- **📘 Complete API Documentation**: [APIDocumentation.md](APIDocumentation.md)
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)
- **Testing Guide**: [tests/TESTING.md](tests/TESTING.md)
- **Project Documentation**: [documenation.md](documenation.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

## 🎯 Quick Reference Commands

```bash
# Setup
python -m venv .venv                    # Create virtual environment
.venv\Scripts\Activate.ps1              # Activate (Windows)
source .venv/bin/activate               # Activate (Linux/Mac)
pip install -r requirements.txt         # Install dependencies

# Development
python run.py                           # Run application
pytest tests/ -v                        # Run tests
ruff check app/ tests/                  # Lint code
ruff check --fix app/ tests/            # Fix linting issues

# Testing
pytest tests/ -v                        # All tests
pytest tests/ -m auth                   # Auth tests only
pytest tests/ --cov=app                 # With coverage
pytest tests/ -k "test_login"           # By name pattern

# Utilities
python -c "import secrets; print(secrets.token_hex(32))"  # Generate SECRET_KEY
curl http://localhost:8000/api/v1/health                  # Health check
```

## 📋 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes | - | JWT signing key (min 32 chars) |
| `GEMINI_API_KEY` | ✅ Yes | - | Google Gemini API key |
| `LLM_MODEL_NAME` | ❌ No | `gemini-2.0-flash-exp` | AI model name |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ No | `30` | Token expiration time |
| `ALGORITHM` | ❌ No | `HS256` | JWT algorithm |
| `RATE_LIMIT_CAPACITY` | ❌ No | `5` | Max requests per period |
| `RATE_LIMIT_REFILL_SECONDS` | ❌ No | `60` | Rate limit refill time |
| `LOG_LEVEL` | ❌ No | `INFO` | Logging level |
| `DEBUG` | ❌ No | `False` | Debug mode |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Run linter: `ruff check app/ tests/`
6. Commit changes: `git commit -am 'Add feature'`
7. Push to branch: `git push origin feature-name`
8. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Version**: 0.1.0  
**Last Updated**: November 2025  
**Python**: 3.9+ (3.11+ recommended)  
**Framework**: FastAPI 0.104+
