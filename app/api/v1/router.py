"""
API v1 router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, analysis, health

api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["Analysis"])
api_router.include_router(health.router, tags=["Health"])
