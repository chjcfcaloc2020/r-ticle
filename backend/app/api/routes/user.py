from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.models import User
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=UserResponse)
def get_user_info(current_user: User = Depends(get_current_active_user)):
  return current_user