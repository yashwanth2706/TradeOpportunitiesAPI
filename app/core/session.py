"""
Session management for tracking user sessions and rate limiting
"""
from datetime import datetime, timezone
from typing import Dict

from app.config import settings
from app.core.rate_limit import RateLimiter


class SessionInfo:
    """
    Manages user session information including rate limiting
    """
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.created_at = datetime.now(timezone.utc)
        self.expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        self.rate_limiter = RateLimiter(
            capacity=settings.RATE_LIMIT_CAPACITY,
            refill_seconds=settings.RATE_LIMIT_REFILL_SECONDS
        )
        self.usage_count = 0
    
    def is_expired(self) -> bool:
        """Check if the session has expired"""
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() > self.expires_in
    
    def allow_request(self) -> bool:
        """
        Check if a request is allowed based on rate limiting
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        allowed = self.rate_limiter.allow_request()
        if allowed:
            self.usage_count += 1
        return allowed


class SessionManager:
    """
    Manages multiple user sessions
    """
    
    def __init__(self):
        self._sessions: Dict[str, SessionInfo] = {}
    
    def get_session(self, client_id: str) -> SessionInfo:
        """
        Get or create a session for a client
        
        Args:
            client_id: Unique identifier for the client
            
        Returns:
            SessionInfo object
        """
        if client_id not in self._sessions:
            self._sessions[client_id] = SessionInfo(client_id)
        return self._sessions[client_id]
    
    def remove_session(self, client_id: str) -> None:
        """Remove a session"""
        self._sessions.pop(client_id, None)
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions
        
        Returns:
            Number of sessions removed
        """
        expired = [
            client_id for client_id, session in self._sessions.items()
            if session.is_expired()
        ]
        for client_id in expired:
            self.remove_session(client_id)
        return len(expired)
    
    @property
    def active_sessions(self) -> int:
        """Get count of active sessions"""
        return len(self._sessions)


# Global session manager instance
session_manager = SessionManager()
