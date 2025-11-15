"""
Health check endpoints
"""
from datetime import datetime, timezone
from fastapi import APIRouter

from app.core.session import session_manager
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health():
    """
    Health check endpoint for monitoring and load balancers.
    
    Used by:
    - Cloud platforms (AWS, Azure, GCP) for health probes
    - Load balancers to route traffic
    - Monitoring tools (Datadog, Prometheus, New Relic)
    - CI/CD pipelines for deployment verification
    
    **Returns:**
    - status: "healthy" if system is operational
    - timestamp: Current server time (UTC)
    - version: API version
    - active_sessions: Number of active user sessions
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.APP_VERSION,
        "active_sessions": session_manager.active_sessions
    }
