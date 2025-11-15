"""
Authentication endpoints
"""
import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.auth import Token, UserRegister
from app.core.auth import authenticate_user, register_user
from app.core.security import create_access_token
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """
    Register a new user and return an access token.
    
    **Requirements:**
    - Username: 3-50 characters
    - Password: minimum 6 characters
    
    **Returns:** JWT access token valid for 60 minutes
    """
    # Register the user (raises exception if username exists)
    register_user(user.username, user.password)
    logger.info("New user registered: %s", user.username)
    
    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login endpoint (required for Swagger UI authorization).
    
    Use this endpoint to authenticate and receive a JWT access token.
    The token is valid for 60 minutes.
    
    **Note:** In the Swagger UI "Authorize" dialog, you only need to provide:
    - username
    - password
    
    Leave `client_id` and `client_secret` empty - they are not required.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user}, 
        expires_delta=access_token_expires
    )
    logger.info("User logged in: %s", user)
    
    return {"access_token": access_token, "token_type": "bearer"}
