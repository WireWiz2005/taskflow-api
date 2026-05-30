from fastapi import APIRouter, Depends
from app.models.schemas import UserResponse
from app.models.models import User
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the currently logged-in user's profile."""
    return current_user
