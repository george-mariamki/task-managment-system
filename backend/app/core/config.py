from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management System"
    API_V1_STR: str = "/api/v1"
    
    # Database settings später hinzufügen

    class Config:
        case_sensitive = True

settings = Settings()
