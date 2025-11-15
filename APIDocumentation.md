# Trade Opportunities API - Complete API Documentation

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
  - [Health & Status](#health--status)
  - [Authentication](#authentication-endpoints)
  - [Analysis](#analysis-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Response Codes](#response-codes)
- [SDK Examples](#sdk-examples)

---

## Overview

The Trade Opportunities API provides AI-powered market analysis for various industry sectors. It uses Google's Gemini AI to analyze market data collected from multiple sources and generate comprehensive trade opportunity reports.

**Key Features:**
- 🔐 JWT-based authentication
- 🚦 Token bucket rate limiting (5 requests/minute)
- 🤖 AI-powered sector analysis
- 📊 Markdown-formatted reports
- ⏱️ Automatic session management
- 🔒 Secure password hashing (bcrypt)

**API Version:** v1  
**Protocol:** HTTPS/HTTP  
**Data Format:** JSON  
**Authentication:** Bearer Token (JWT)

---

## Base URL

```
Local Development: http://localhost:8000
Production: https://your-domain.com
```

All API endpoints are prefixed with `/api/v1/`

**Example:**
```
http://localhost:8000/api/v1/auth/register
http://localhost:8000/api/v1/analyze/technology
```

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication. Most endpoints require a valid Bearer token in the Authorization header.

### Authentication Flow

```
1. Register → POST /api/v1/auth/register
2. Login → POST /api/v1/auth/token (get JWT token)
3. Use token → Include in Authorization header for protected endpoints
```

### Token Format

```
Authorization: Bearer <your_jwt_token>
```

### Token Expiration

- **Default:** 30 minutes
- **Configurable:** via `ACCESS_TOKEN_EXPIRE_MINUTES` environment variable
- **Refresh:** Login again to get a new token

---

## Rate Limiting

**Algorithm:** Token Bucket  
**Limit:** 5 requests per 60 seconds per user  
**Scope:** Per authenticated user

### Rate Limit Headers

```http
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 3
X-RateLimit-Reset: 1699876543
```

### Rate Limit Response

When rate limit is exceeded:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "detail": "Rate limit exceeded. Please try again later."
}
```

**Token Bucket Details:**
- Initial capacity: 5 tokens
- Refill rate: Full capacity every 60 seconds
- Tokens consumed: 1 per request

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Scenarios

| Error | Status Code | Description |
|-------|-------------|-------------|
| Invalid credentials | 401 | Wrong username or password |
| Missing token | 401 | Authorization header not provided |
| Invalid token | 401 | Token is malformed or expired |
| Session expired | 401 | User session has expired |
| Rate limit exceeded | 429 | Too many requests |
| Invalid input | 422 | Validation error in request data |
| Server error | 500 | Internal server error |

---

## Endpoints

### Health & Status

#### GET /api/v1/

Get API welcome message and basic information.

**Authentication:** Not required

**Request:**
```http
GET /api/v1/ HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "message": "Trade Opportunities API",
  "docs": "/docs",
  "version": "0.1.0"
}
```

**Status Codes:**
- `200 OK` - Success

---

#### GET /api/v1/health

Check API health and get active session count.

**Authentication:** Not required

**Request:**
```http
GET /api/v1/health HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "status": "ok",
  "active_sessions": 3
}
```

**Status Codes:**
- `200 OK` - API is healthy

---

### Authentication Endpoints

#### POST /api/v1/auth/register

Register a new user account.

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string (3-50 characters, alphanumeric + underscore)",
  "password": "string (6-100 characters)"
}
```

**Validation Rules:**
- Username: 3-50 characters, alphanumeric and underscore only
- Password: 6-100 characters, any characters allowed

**Request Example:**
```http
POST /api/v1/auth/register HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (Success):**
```json
{
  "username": "johndoe",
  "message": "User registered successfully"
}
```

**Response (User Exists):**
```json
{
  "detail": "Username already registered"
}
```

**Status Codes:**
- `200 OK` - User registered successfully
- `400 Bad Request` - Username already exists
- `422 Unprocessable Entity` - Validation error

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

---

#### POST /api/v1/auth/token

Login and get JWT access token.

**Authentication:** Not required

**Request Body (Form Data):**
```
username: string
password: string
```

**Content-Type:** `application/x-www-form-urlencoded`

**Request Example:**
```http
POST /api/v1/auth/token HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepass123
```

**Response (Success):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (Invalid Credentials):**
```json
{
  "detail": "Incorrect username or password"
}
```

**Status Codes:**
- `200 OK` - Login successful, token returned
- `401 Unauthorized` - Invalid credentials
- `422 Unprocessable Entity` - Missing required fields

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepass123"
```

**JWT Token Structure:**

The token contains:
```json
{
  "sub": "username",
  "exp": 1699876543
}
```

- `sub`: Username (subject)
- `exp`: Expiration timestamp (Unix timestamp)

---

### Analysis Endpoints

#### GET /api/v1/analyze/{sector}

Analyze a specific sector and generate a comprehensive market report.

**Authentication:** Required (Bearer Token)

**Path Parameters:**
- `sector` (string, required): Sector name to analyze
  - Length: 2-30 characters
  - Format: Alphabetic characters only
  - Examples: `technology`, `pharmaceuticals`, `agriculture`

**Request Example:**
```http
GET /api/v1/analyze/technology HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Success):**
```json
{
  "sector": "technology",
  "report_markdown": "# Technology Sector Trade Opportunities\n\n## Executive Summary\n...",
  "generated_at": "2025-11-15T10:30:45.123456",
  "model_used": "gemini-2.0-flash-exp"
}
```

**Response Fields:**
- `sector` (string): The analyzed sector name
- `report_markdown` (string): Full markdown-formatted analysis report
- `generated_at` (string): ISO 8601 timestamp of report generation
- `model_used` (string): AI model used for analysis

**Report Structure:**

The markdown report typically includes:
1. **Summary** - Overview of the sector
2. **Key Drivers** - Main factors influencing the sector
3. **Top Opportunities** - Specific trade opportunities
4. **Risks** - Potential risks and challenges
5. **Suggested Trades** - Long/short trading ideas
6. **Data Sources** - References to source material

**File Storage:**

Reports are also saved to disk:
- **Location:** `reports/` directory
- **Filename Format:** `{sector}_sector_report_by_{model}.md`
- **Duplicate Handling:** Auto-increments with counter: `sector_(2)_by_model.md`

**Error Responses:**

**Invalid Token:**
```json
{
  "detail": "Could not validate credentials"
}
```

**Session Expired:**
```json
{
  "detail": "Session expired. Please login again."
}
```

**Rate Limited:**
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

**Invalid Sector:**
```json
{
  "detail": [
    {
      "loc": ["path", "sector"],
      "msg": "string does not match regex '^[a-zA-Z]{2,30}$'",
      "type": "value_error.str.regex"
    }
  ]
}
```

**Analysis Failed:**
```json
{
  "sector": "technology",
  "report_markdown": "Unable to perform analysis. Error: API key not configured",
  "generated_at": "2025-11-15T10:30:45.123456",
  "model_used": "gemini-2.0-flash-exp"
}
```

**Status Codes:**
- `200 OK` - Analysis completed successfully
- `401 Unauthorized` - Authentication failed or session expired
- `422 Unprocessable Entity` - Invalid sector format
- `429 Too Many Requests` - Rate limit exceeded

**Example with curl:**
```bash
# Get token first
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepass123" \
  | jq -r '.access_token')

# Analyze sector
curl -X GET "http://localhost:8000/api/v1/analyze/technology" \
  -H "Authorization: Bearer $TOKEN"
```

**Supported Sectors:**

Any alphabetic sector name (2-30 characters):
- `technology`
- `pharmaceuticals`
- `agriculture`
- `automotive`
- `energy`
- `finance`
- `healthcare`
- `manufacturing`
- `retail`
- `telecommunications`
- etc.

---

## Request/Response Examples

### Complete Workflow Example

#### 1. Register a User

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "trader001",
    "password": "MySecureP@ss123"
  }'
```

**Response:**
```json
{
  "username": "trader001",
  "message": "User registered successfully"
}
```

---

#### 2. Login and Get Token

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=trader001&password=MySecureP@ss123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0cmFkZXIwMDEiLCJleHAiOjE2OTk4NzY1NDN9.xyz...",
  "token_type": "bearer"
}
```

---

#### 3. Analyze Technology Sector

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/analyze/technology" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0cmFkZXIwMDEiLCJleHAiOjE2OTk4NzY1NDN9.xyz..."
```

**Response:**
```json
{
  "sector": "technology",
  "report_markdown": "# Technology Sector Trade Opportunities\n\n## Executive Summary\n\nThe technology sector shows strong momentum...\n\n## Key Drivers\n\n1. **AI Revolution**: Artificial intelligence adoption...\n2. **Cloud Computing**: Migration to cloud services...\n3. **5G Deployment**: Enhanced connectivity...\n\n## Top Opportunities\n\n### 1. Semiconductor Stocks\n- **Rationale**: Global chip shortage continues\n- **Timeline**: 6-12 months\n- **Risk Level**: Medium\n\n### 2. Cybersecurity Firms\n- **Rationale**: Rising cyber threats\n- **Timeline**: Long-term\n- **Risk Level**: Low\n\n## Risks\n\n- Regulatory scrutiny\n- Market saturation\n- Economic downturn\n\n## Suggested Trades\n\n**Long Positions:**\n- Large-cap tech companies with strong AI initiatives\n- Cloud infrastructure providers\n\n**Short Positions:**\n- Legacy hardware manufacturers\n- Companies with weak cybersecurity\n\n## Data Sources\n\n- Industry reports\n- Market analysis\n- Recent news articles",
  "generated_at": "2025-11-15T10:30:45.123456",
  "model_used": "gemini-2.0-flash-exp"
}
```

---

#### 4. Check Health Status

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

**Response:**
```json
{
  "status": "ok",
  "active_sessions": 5
}
```

---

## Response Codes

### Success Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |

### Client Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 400 | Bad Request | Invalid request format or duplicate resource |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Endpoint not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## SDK Examples

### Python

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

class TradeOpportunitiesAPI:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def register(self, username, password):
        """Register a new user"""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "password": password}
        )
        return response.json()
    
    def login(self, username, password):
        """Login and get access token"""
        response = requests.post(
            f"{self.base_url}/auth/token",
            data={"username": username, "password": password}
        )
        data = response.json()
        self.token = data.get("access_token")
        return data
    
    def analyze_sector(self, sector):
        """Analyze a specific sector"""
        if not self.token:
            raise Exception("Not authenticated. Please login first.")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            f"{self.base_url}/analyze/{sector}",
            headers=headers
        )
        return response.json()
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage example
api = TradeOpportunitiesAPI()

# Register
print(api.register("myuser", "mypassword"))

# Login
print(api.login("myuser", "mypassword"))

# Analyze sector
report = api.analyze_sector("technology")
print(f"Generated report for: {report['sector']}")
print(f"Model used: {report['model_used']}")
print(report['report_markdown'][:200])  # First 200 chars

# Health check
print(api.health_check())
```

---

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';

class TradeOpportunitiesAPI {
    constructor(baseUrl = BASE_URL) {
        this.baseUrl = baseUrl;
        this.token = null;
    }

    async register(username, password) {
        const response = await axios.post(`${this.baseUrl}/auth/register`, {
            username,
            password
        });
        return response.data;
    }

    async login(username, password) {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        const response = await axios.post(`${this.baseUrl}/auth/token`, params, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        
        this.token = response.data.access_token;
        return response.data;
    }

    async analyzeSector(sector) {
        if (!this.token) {
            throw new Error('Not authenticated. Please login first.');
        }

        const response = await axios.get(`${this.baseUrl}/analyze/${sector}`, {
            headers: { 'Authorization': `Bearer ${this.token}` }
        });
        return response.data;
    }

    async healthCheck() {
        const response = await axios.get(`${this.baseUrl}/health`);
        return response.data;
    }
}

// Usage example
(async () => {
    const api = new TradeOpportunitiesAPI();

    // Register
    console.log(await api.register('myuser', 'mypassword'));

    // Login
    console.log(await api.login('myuser', 'mypassword'));

    // Analyze sector
    const report = await api.analyzeSector('technology');
    console.log(`Generated report for: ${report.sector}`);
    console.log(`Model used: ${report.model_used}`);
    console.log(report.report_markdown.substring(0, 200));

    // Health check
    console.log(await api.healthCheck());
})();
```

---

### cURL Scripts

**Complete workflow script:**

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"
USERNAME="testuser"
PASSWORD="testpass123"
SECTOR="technology"

echo "=== 1. Registering user ==="
curl -X POST "${BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}"

echo -e "\n\n=== 2. Logging in ==="
TOKEN=$(curl -X POST "${BASE_URL}/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${USERNAME}&password=${PASSWORD}" \
  | jq -r '.access_token')

echo "Token: ${TOKEN}"

echo -e "\n\n=== 3. Analyzing sector ==="
curl -X GET "${BASE_URL}/analyze/${SECTOR}" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq '.'

echo -e "\n\n=== 4. Checking health ==="
curl -X GET "${BASE_URL}/health" | jq '.'
```

---

## Interactive API Documentation

The API provides interactive documentation at:

- **Swagger UI:** http://localhost:8000/docs
  - Interactive API explorer
  - Try out endpoints directly
  - View request/response schemas
  - Download OpenAPI spec

- **ReDoc:** http://localhost:8000/redoc
  - Clean, organized documentation
  - Searchable endpoints
  - Code samples
  - Detailed schemas

---

## Best Practices

### 1. Token Management

- Store tokens securely (environment variables, secure storage)
- Implement token refresh logic before expiration
- Never commit tokens to version control
- Use HTTPS in production to protect tokens

### 2. Error Handling

```python
try:
    response = api.analyze_sector("technology")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        # Token expired, re-login
        api.login(username, password)
        response = api.analyze_sector("technology")
    elif e.response.status_code == 429:
        # Rate limited, wait and retry
        time.sleep(60)
        response = api.analyze_sector("technology")
    else:
        raise
```

### 3. Rate Limiting

- Implement exponential backoff for retries
- Monitor rate limit headers
- Queue requests when approaching limits
- Use batch operations when available

### 4. Security

- Always use HTTPS in production
- Validate and sanitize all inputs
- Store API keys securely
- Implement proper logging (without sensitive data)
- Use strong passwords (min 12 characters recommended)

---

## Support & Resources

- **GitHub Repository:** https://github.com/yashwanth2706/TradeOpportunitiesAPI
- **Issues:** Report bugs and request features on GitHub
- **API Docs:** http://localhost:8000/docs (when running locally)

---

**Last Updated:** November 15, 2025  
**API Version:** v1  
**Document Version:** 1.0.0
