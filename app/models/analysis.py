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
        max_length=50,  # Increased to allow for spaces
        description="Sector name (2-50 chars, letters and spaces only, max 4 consecutive spaces)"
    )
    
    @field_validator('sector')
    @classmethod
    def validate_sector(cls, v: str) -> str:
        """
        Validate and normalize sector name
        
        Rules:
        - Must be 2-50 characters after stripping
        - Only letters and spaces allowed
        - Maximum 4 consecutive spaces
        - Normalizes to lowercase with single spaces
        
        Examples:
        Accept: "Cloud Computing" -> "cloud computing"
        Accept: "Agriculture and Fertilizer" -> "agriculture and fertilizer"
        Accept: "Cloud    Computing" (4 spaces) -> "cloud computing"
        ------------------------------------------------------------
        Reject: "Cloud     Computing" (5 spaces) -> ValueError
        Reject: "   " (only spaces) -> ValueError
        Reject: "Tech123" (numbers) -> ValueError
        """
        # Strip leading/trailing whitespace
        v = v.strip()
        
        # Check minimum length after stripping
        if len(v) < 2:
            raise ValueError("Sector must be at least 2 characters long")
        
        # Check maximum length
        if len(v) > 50:
            raise ValueError("Sector must not exceed 50 characters")
        
        # Check for only spaces
        if not v.replace(' ', ''):
            raise ValueError("Sector cannot contain only spaces")
        
        # Check for only letters and spaces
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError("Sector must contain only letters and spaces")
        
        # Check for more than 4 consecutive spaces
        if '     ' in v:  # 5 consecutive spaces
            raise ValueError("Sector cannot have more than 4 consecutive spaces")
        
        # Normalize: lowercase and collapse multiple spaces to single space
        normalized = ' '.join(v.lower().split())
        
        return normalized


class AnalyzeResponse(BaseModel):
    """Analysis response model"""
    sector: str
    generated_at: datetime
    report_markdown: str
