from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field

from app.api.dependencies import get_current_user, rate_limit
from app.core.security import PasswordHasher, TokenManager, UnauthorizedError

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(request: RegisterRequest):
    hashed_password = PasswordHasher.hash_password(request.password)
    access_token = TokenManager.create_access_token(subject=request.email, role="user")
    refresh_token = TokenManager.create_refresh_token(subject=request.email)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    access_token = TokenManager.create_access_token(subject=request.email, role="user")
    refresh_token = TokenManager.create_refresh_token(subject=request.email)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    payload = TokenManager.decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise UnauthorizedError("Invalid refresh token")
    new_access = TokenManager.create_access_token(subject=payload["sub"], role="user")
    new_refresh = TokenManager.create_refresh_token(subject=payload["sub"])
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user), _=Depends(rate_limit)):
    return {"message": "Logged out successfully"}
