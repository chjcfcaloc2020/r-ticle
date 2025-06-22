from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.core.database import engine
from app.core.config import settings
from app.api import api_router

Base.metadata.create_all(engine)

app = FastAPI(
  title=settings.PROJECT_NAME,
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
  return {"message": "Hello, FastAPI!"}