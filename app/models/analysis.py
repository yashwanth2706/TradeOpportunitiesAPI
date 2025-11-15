"""
Pydantic models for analysis endpoints
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SectorParam(BaseModel):
    """Sector parameter validation"""
    sector: str = Field(
        ..., 
        min_length=2, 
        max_length=30,
        pattern="^[A-Za-z]+$",
        description="Sector must contain only alphabets, 2-30 characters."
    )
    
    @field_validator('sector')
    @classmethod
    def validate_sector(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("Sector must be at least 2 characters long")
        if not v.isalpha():
            raise ValueError("Sector must contain only alphabetic characters")
        if len(v) > 30:
            raise ValueError("Sector must not exceed 30 characters")
        return v.strip().lower()


class AnalyzeResponse(BaseModel):
    """Analysis response model"""
    sector: str
    generated_at: datetime
    report_markdown: str
