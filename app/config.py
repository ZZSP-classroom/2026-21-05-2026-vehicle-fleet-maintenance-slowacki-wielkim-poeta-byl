# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # This will look for an environment variable named SQLALCHEMY_DATABASE_URI
    # If it doesn't find one, it defaults to the local SQLite file below
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env" # Allows you to load variables from a .env file

settings = Settings()