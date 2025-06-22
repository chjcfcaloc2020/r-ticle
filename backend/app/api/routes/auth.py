from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, TokenResponse
from app.models import User
from app.crud import user as crud_user
from app.core.database import init_db
from app.auth.hashing import verify_password
from app.utils.jwt import create_jwt_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def create(user: UserCreate, db: Session = Depends(init_db)):
  check_exsist_user = crud_user.get_user_by_username(db, user.username)
  if check_exsist_user:
    raise HTTPException(status_code=400, detail="Username already registered")
  response = crud_user.create_user(db, user)
  return {"username": response.name, "message": "User created successfully"}

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(init_db)):
  user = db.query(User).filter(
    (User.username == form_data.username) | (User.email == form_data.username)
  ).first()
  if not user or not verify_password(form_data.password, user.password):
    raise HTTPException(status_code=400, detail="Invalid username or password")
  access_token = create_jwt_token(
    payload={"sub": user.username},
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
  )
  return {"access_token": access_token, "token_type": "bearer"}