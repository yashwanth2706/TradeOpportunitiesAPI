"""
Analysis endpoints
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.models.analysis import AnalyzeResponse, SectorParam
from app.dependencies import get_current_user
from app.services import DataCollector, LLMClient
from app.core.session import session_manager
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
data_collector = DataCollector()
llm_client = LLMClient()


@router.get("/{sector}", response_model=AnalyzeResponse)
async def analyze_sector(
    sector: str,
    request: Request,
    current_user: str = Depends(get_current_user)
):
    """
    Analyze trade opportunities for a given sector.
    
    **Requires JWT authentication.**
    
    **Parameters:**
    - sector: Sector name (2-30 alphabetic characters only)
    
    **Returns:** Comprehensive market analysis report
    
    **Rate Limit:** 5 requests per minute per user
    """
    # Input validation
    try:
        param = SectorParam(sector=sector)
    except Exception as e:
        logger.warning("Invalid sector parameter '%s': %s", sector, e)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sector parameter. Sector must be 2-30 alphabetic characters. Error: {str(e)}"
        )
    
    # Session management and rate limiting
    session = session_manager.get_session(current_user)
    
    if session.is_expired():
        session_manager.remove_session(current_user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please login again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Enforce rate limit
    if not session.allow_request():
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )
    
    logger.info("Analyze requested for sector=%s by user=%s", param.sector, current_user)
    
    # Step 1: Collect data
    query = f"{param.sector} sector current market data and news"
    try:
        snippets = await data_collector.search_news(query, limit=6)
    except Exception as e:
        logger.error("Data collection failed: %s", e)
        raise HTTPException(status_code=502, detail="Failed to collect market data")
    
    # Step 2: LLM analysis
    try:
        report = await llm_client.analyze(param.sector, snippets)
    except Exception as e:
        logger.exception("LLM analysis failed: %s", e)
        raise HTTPException(status_code=502, detail="LLM analysis failed")
    
    # Step 3: Return response
    return AnalyzeResponse(
        sector=param.sector,
        generated_at=datetime.utcnow(),
        report_markdown=report,
    )
