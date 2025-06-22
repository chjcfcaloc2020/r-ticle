from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
  username: str
  name: str
  email: EmailStr

class UserCreate(User):
  password: str

class UserResponse(BaseModel):
  username: str
  name: str
  email: EmailStr
  role: str
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True

class UserLogin(BaseModel):
  username: str
  password: str

class TokenResponse(BaseModel):
  access_token: str
  token_type: str