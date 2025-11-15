"""
Pydantic models for authentication
"""
from pydantic import BaseModel, Field


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str


class UserRegister(BaseModel):
    """User registration model"""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    password: str = Field(..., min_length=6, max_length=100, description="Password (minimum 6 characters)")
