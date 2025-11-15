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
- JWT-based authentication with 60-minute token expiration
- Token bucket rate limiting (5 requests per 60 seconds per user)
- AI-powered sector analysis using Google Gemini
- Markdown-formatted reports with automatic file saving
- Automatic session management with timezone-aware timestamps
- Secure password hashing using bcrypt
- Production-grade health monitoring endpoint

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

- **Default:** 60 minutes
- **Configurable:** via `ACCESS_TOKEN_EXPIRE_MINUTES` environment variable
- **Refresh:** Login again to get a new token
- **Session Management:** Sessions automatically expire after token expiration

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

#### GET /

Root endpoint - Redirects to interactive API documentation.

**Authentication:** Not required

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response:**
```http
HTTP/1.1 307 Temporary Redirect
Location: /docs
```

**Status Codes:**
- `307 Temporary Redirect` - Redirects to /docs

---

#### GET /api/v1/health

Production-grade health check endpoint for monitoring, load balancers, and CI/CD pipelines.

**Authentication:** Not required

**Use Cases:**
- Cloud platform health probes (AWS, Azure, GCP)
- Load balancer traffic routing decisions
- Monitoring tools (Datadog, Prometheus, New Relic)
- Deployment verification in CI/CD pipelines

**Request:**
```http
GET /api/v1/health HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T14:30:45.123456+00:00",
  "version": "0.1.0",
  "active_sessions": 3
}
```

**Response Fields:**
- `status` (string): "healthy" if system is operational
- `timestamp` (string): Current server time in ISO 8601 format (UTC)
- `version` (string): API version number
- `active_sessions` (integer): Number of active authenticated user sessions

**Status Codes:**
- `200 OK` - API is healthy and operational

---

### Authentication Endpoints

#### POST /api/v1/auth/register

Register a new user account and receive instant access token.

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string (3-50 characters, alphanumeric)",
  "password": "string (6-100 characters)"
}
```

**Validation Rules:**
- Username: 3-50 characters, alphanumeric characters only
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
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (User Exists):**
```json
{
  "detail": "Username already registered"
}
```

**Status Codes:**
- `201 Created` - User registered successfully, token returned
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
  - Length: 2-50 characters after trimming whitespace
  - Format: Letters and spaces only (maximum 4 consecutive spaces)
  - Normalization: Converted to lowercase with single spaces
  - Examples: `technology`, `cloud computing`, `agriculture and fertilizer`

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
  "generated_at": "2025-11-15T10:30:45.123456"
}
```

**Response Fields:**
- `sector` (string): The analyzed sector name (normalized to lowercase)
- `report_markdown` (string): Full markdown-formatted analysis report
- `generated_at` (datetime): ISO 8601 timestamp of report generation (UTC)

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
  "detail": "Invalid sector parameter. Sector must be 2-50 alphabetic characters. Error: Sector must contain only letters and spaces"
}
```

**Common Validation Errors:**
- Too short: "Sector must be at least 2 characters long"
- Too long: "Sector must not exceed 50 characters"
- Invalid characters: "Sector must contain only letters and spaces"
- Too many spaces: "Sector cannot have more than 4 consecutive spaces"
- Only spaces: "Sector cannot contain only spaces"

**Analysis Failed:**
```json
{
  "detail": "LLM analysis failed"
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

Any sector name with letters and spaces (2-50 characters):

**Single Word Sectors:**
- `technology`
- `pharmaceuticals`
- `agriculture`
- `automotive`
- `energy`
- `finance`
- `healthcare`
- `manufacturing`
- `retail`

**Multi-Word Sectors:**
- `cloud computing`
- `renewable energy`
- `artificial intelligence`
- `machine learning`
- `data science`
- `cyber security`
- `financial services`
- `agriculture and fertilizer`

**Note:** Spaces are automatically normalized (multiple spaces collapsed to single space)

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
  "generated_at": "2025-11-15T10:30:45.123456"
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
  "status": "healthy",
  "timestamp": "2025-11-15T14:30:45.123456+00:00",
  "version": "0.1.0",
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

# Register (automatically gets token)
print(api.register("myuser", "mypassword"))

# Login (if needed later)
print(api.login("myuser", "mypassword"))

# Analyze sector
report = api.analyze_sector("technology")
print(f"Generated report for: {report['sector']}")
print(f"Generated at: {report['generated_at']}")
print(report['report_markdown'][:200])  # First 200 chars

# Health check
health = api.health_check()
print(f"API Status: {health['status']}")
print(f"Active Sessions: {health['active_sessions']}")
print(f"Server Time: {health['timestamp']}")
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

    // Register (automatically gets token)
    console.log(await api.register('myuser', 'mypassword'));

    // Login (if needed later)
    console.log(await api.login('myuser', 'mypassword'));

    // Analyze sector
    const report = await api.analyzeSector('technology');
    console.log(`Generated report for: ${report.sector}`);
    console.log(`Generated at: ${report.generated_at}`);
    console.log(report.report_markdown.substring(0, 200));

    // Health check
    const health = await api.healthCheck();
    console.log(`API Status: ${health.status}`);
    console.log(`Active Sessions: ${health.active_sessions}`);
    console.log(`Server Time: ${health.timestamp}`);
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

- **Root URL:** http://localhost:8000/
  - Automatically redirects to /docs

- **Swagger UI:** http://localhost:8000/docs
  - Interactive API explorer with "Try it out" functionality
  - Built-in authentication with Authorize button
  - View request/response schemas
  - Download OpenAPI specification

- **ReDoc:** http://localhost:8000/redoc
  - Clean, organized documentation
  - Searchable endpoints
  - Detailed schemas with examples
  - No interactive testing (read-only)

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
