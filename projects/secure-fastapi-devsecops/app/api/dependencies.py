from fastapi import Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenManager, UnauthorizedError
from app.core.rate_limit import RateLimitMiddleware


async def get_current_user(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid authorization header")

    token = authorization.split(" ")[1]
    payload = TokenManager.decode_token(token)

    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    return {"id": payload["sub"], "role": payload.get("role", "user")}


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise UnauthorizedError("Admin privileges required")
    return current_user


async def rate_limit(request: Request, current_user: dict = Depends(get_current_user)) -> None:
    client_ip = request.client.host if request.client else "unknown"
    await RateLimitMiddleware().check_rate_limit(current_user["id"], client_ip)
