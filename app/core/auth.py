"""
Authentication logic and user management
"""
from typing import Optional, Dict
from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password


# In-memory user store (username -> hashed_password)
# TODO: Replace with database in production
users_db: Dict[str, str] = {}


def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate a user with username and password
    
    Args:
        username: Username to authenticate
        password: Plain text password
        
    Returns:
        Username if authentication successful, None otherwise
    """
    hashed_password = users_db.get(username)
    if not hashed_password:
        return None
    
    if not verify_password(password, hashed_password):
        return None
    
    return username


def register_user(username: str, password: str) -> None:
    """
    Register a new user
    
    Args:
        username: Username for new user
        password: Plain text password
        
    Raises:
        HTTPException: If username already exists
    """
    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = hash_password(password)
    users_db[username] = hashed_password


def user_exists(username: str) -> bool:
    """Check if a user exists"""
    return username in users_db
