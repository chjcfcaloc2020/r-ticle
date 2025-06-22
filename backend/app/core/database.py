from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.core.config import settings
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def init_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    