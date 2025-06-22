from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  SECRET_KEY: str
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int
  PROJECT_NAME: str = "R-TICLE Backend"
  DATABASE_URL: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

settings = Settings()