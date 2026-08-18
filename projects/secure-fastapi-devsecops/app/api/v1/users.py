from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from app.api.dependencies import get_current_user, rate_limit, require_admin

router = APIRouter()


class UserResponse(BaseModel):
    id: str
    email: str
    role: str


@router.get("/", response_model=list[UserResponse])
async def list_users(
    current_user: dict = Depends(require_admin),
    _=Depends(rate_limit),
):
    return []


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    _=Depends(rate_limit),
):
    return {"id": user_id, "email": "user@example.com", "role": "user"}


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    _=Depends(rate_limit),
):
    return None
