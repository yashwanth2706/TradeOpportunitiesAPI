"""
Rate limiting implementation using token bucket algorithm
"""
import time


class RateLimiter:
    """
    Token bucket rate limiter
    
    Allows a certain number of requests per time period,
    with automatic token refill over time.
    """
    
    def __init__(self, capacity: int, refill_seconds: int):
        """
        Initialize rate limiter
        
        Args:
            capacity: Maximum number of tokens (requests) allowed
            refill_seconds: Time interval for token refill
        """
        self.capacity = capacity
        self.refill_seconds = refill_seconds
        self.tokens = capacity
        self.last_refill = time.monotonic()
    
    def allow_request(self) -> bool:
        """
        Check if a request is allowed and consume a token
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        now = time.monotonic()
        elapsed = now - self.last_refill
        
        # Refill tokens based on time elapsed
        if elapsed >= self.refill_seconds:
            steps = int(elapsed // self.refill_seconds)
            refill_amount = steps * self.capacity
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            self.last_refill = now
        
        # Check if we have tokens available
        if self.tokens > 0:
            self.tokens -= 1
            return True
        
        return False
    
    @property
    def available_tokens(self) -> int:
        """Get current number of available tokens"""
        return self.tokens
