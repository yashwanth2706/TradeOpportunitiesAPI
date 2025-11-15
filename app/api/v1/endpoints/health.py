"""
Health check endpoints
"""
from fastapi import APIRouter

from app.core.session import session_manager

router = APIRouter()


@router.get("/")
async def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "Trade Opportunities API",
        "docs": "/docs",
        "version": "0.1.0"
    }


@router.get("/health")
async def health():
    """
    Health check endpoint
    
    Returns system status and active session count
    """
    return {
        "status": "ok",
        "active_sessions": session_manager.active_sessions
    }
