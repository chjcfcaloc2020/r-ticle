from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database import init_db
from app.utils.jwt import decode_and_verify_token
from app.models import User
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
  token: Annotated[str, Depends(oauth2_scheme)],
  db: Session = Depends(init_db)
):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = decode_and_verify_token(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db.query(User).filter(User.username == username).first()
  if user is None:
    raise credentials_exception
  
  return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
  return current_user