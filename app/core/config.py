from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VehicleFleetMaintenance"
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///fleet.db"
    SECRET_KEY: str = "supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        case_sensitive = True

settings = Settings()