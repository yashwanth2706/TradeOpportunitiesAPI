"""
Application Configuration
Centralized configuration management for the application.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings:
    """Application settings"""
    
    # Application
    APP_NAME: str = "Trade Opportunities API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Rate Limiting
    RATE_LIMIT_CAPACITY: int = 5  # requests
    RATE_LIMIT_REFILL_SECONDS: int = 60  # seconds
    
    # API Keys (for external services)
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY")
    LLM_API_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        if not self.SECRET_KEY:
            raise RuntimeError("SECRET_KEY environment variable is required")
    
    @property
    def api_v1_prefix(self) -> str:
        return "/api/v1"


# Global settings instance
settings = Settings()
