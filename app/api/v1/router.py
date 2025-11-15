"""
API v1 router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, analysis

api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["Analysis"])
