"""
Main FastAPI application
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.api.v1.router import api_router
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        API for analyzing trade opportunities across different sectors.
        
        ## Authentication
        1. **Register**: Create a new account at `/api/v1/auth/register` - returns an access token
        2. **Login**: Get a token at `/api/v1/auth/token` using your credentials
        3. **Authorize**: Click the 🔒 Authorize button and enter your username/password
           - Leave `client_id` and `client_secret` fields empty (not required)
        4. Use the token to access protected endpoints like `/api/v1/analyze/{sector}`
        
        ## Rate Limiting
        - 5 requests per minute per user
        - Tokens refill automatically
        
        ## API Versioning
        - Current version: v1
        - Base path: `/api/v1`
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    # Root endpoint - redirect to docs
    @app.get("/", include_in_schema=False)
    async def root():
        """Redirect root to API documentation"""
        return RedirectResponse(url="/docs")
    
    # Startup event
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info(f"Debug mode: {settings.DEBUG}")
        yield
        # Shutdown
        logger.info(f"Shutting down {settings.APP_NAME}")
    
    # Shutdown event
    app.router.lifespan_context = lifespan
    async def shutdown_event():
        logger.info(f"Shutting down {settings.APP_NAME}")
    
    return app


# Create app instance
app = create_app()
