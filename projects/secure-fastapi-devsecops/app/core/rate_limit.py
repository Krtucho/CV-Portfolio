import time
from collections import defaultdict
from typing import Dict, Tuple
from app.core.config import settings
from app.core.security import RateLimitExceeded


class InMemoryRateLimiter:
    def __init__(self):
        self._windows: Dict[str, Tuple[float, int]] = {}

    def check(self, key: str, max_requests: int, window_seconds: int) -> None:
        now = time.time()
        window_start, count = self._windows.get(key, (now, 0))

        if now - window_start > window_seconds:
            window_start = now
            count = 0

        count += 1

        if count > max_requests:
            raise RateLimitExceeded()

        self._windows[key] = (window_start, count)


rate_limiter = InMemoryRateLimiter()


class RateLimitMiddleware:
    async def check_rate_limit(self, user_id: str, ip: str) -> None:
        rate_limiter.check(f"user:{user_id}", settings.RATE_LIMIT_PER_USER, settings.RATE_LIMIT_WINDOW_SECONDS)
        rate_limiter.check(f"ip:{ip}", settings.RATE_LIMIT_PER_IP, settings.RATE_LIMIT_WINDOW_SECONDS)
