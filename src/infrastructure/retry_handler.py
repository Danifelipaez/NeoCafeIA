import time
import logging
from typing import Callable, TypeVar, Any, Optional
from functools import wraps


T = TypeVar('T')
logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry logic"""
    def __init__(self, max_attempts: int = 3, initial_delay: float = 1.0, exponential_base: float = 2.0):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.exponential_base = exponential_base


def is_retryable_error(exception: Exception) -> bool:
    """Determine if an error is retryable (e.g., 429 rate limit, timeout)"""
    error_str = str(exception)
    
    # Rate limit error (429)
    if "429" in error_str or "rate_limit" in error_str.lower():
        return True
    
    # Timeout-like errors
    if any(x in error_str.lower() for x in ["timeout", "connection", "temporary"]):
        return True
    
    # OpenAI-specific rate limit error
    if "RateLimitError" in type(exception).__name__:
        return True
    
    # Anthropic-specific rate limit error
    if "RateLimitError" in type(exception).__name__:
        return True
    
    # Google (Gemini) rate limit
    if "RESOURCE_EXHAUSTED" in error_str:
        return True
    
    return False


def retry_with_backoff(config: Optional[RetryConfig] = None) -> Callable:
    """
    Decorator for retrying functions with exponential backoff.
    
    Retries on rate limit errors (429) and timeouts.
    Other errors are immediately re-raised.
    
    Usage:
        @retry_with_backoff(RetryConfig(max_attempts=3))
        def some_api_call():
            return response
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if not is_retryable_error(e):
                        # Don't retry non-retryable errors
                        raise
                    
                    if attempt == config.max_attempts - 1:
                        # Last attempt, re-raise
                        logger.warning(f"Max retry attempts ({config.max_attempts}) reached for {func.__name__}")
                        raise
                    
                    # Calculate backoff delay
                    delay = config.initial_delay * (config.exponential_base ** attempt)
                    logger.info(
                        f"Retryable error in {func.__name__} (attempt {attempt + 1}/{config.max_attempts}). "
                        f"Retrying in {delay}s. Error: {str(e)[:100]}"
                    )
                    time.sleep(delay)
            
            # Should not reach here, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def call_with_retry(func: Callable[..., T], config: Optional[RetryConfig] = None, *args: Any, **kwargs: Any) -> T:
    """
    Call a function with retry logic (alternative to decorator).
    
    Usage:
        result = call_with_retry(api_call, RetryConfig(max_attempts=3), arg1, arg2)
    """
    if config is None:
        config = RetryConfig()
    
    last_exception = None
    
    for attempt in range(config.max_attempts):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            
            if not is_retryable_error(e):
                raise
            
            if attempt == config.max_attempts - 1:
                logger.warning(f"Max retry attempts ({config.max_attempts}) reached for {func.__name__}")
                raise
            
            delay = config.initial_delay * (config.exponential_base ** attempt)
            logger.info(
                f"Retryable error in {func.__name__} (attempt {attempt + 1}/{config.max_attempts}). "
                f"Retrying in {delay}s. Error: {str(e)[:100]}"
            )
            time.sleep(delay)
    
    if last_exception:
        raise last_exception
