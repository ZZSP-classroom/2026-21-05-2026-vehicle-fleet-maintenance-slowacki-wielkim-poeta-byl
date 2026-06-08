from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VehicleFleetMaintenance"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./fleet.db"
    
    class Config:
        case_sensitive = True

settings = Settings()
