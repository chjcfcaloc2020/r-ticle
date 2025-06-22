from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models import User
from app.auth.hashing import hash_password

def get_user_by_username(db: Session, username: str):
  return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
  hashed_pw = hash_password(user.password)
  new_user = User(
    username=user.username,
    password=hashed_pw,
    name=user.name,
    email=user.email
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
