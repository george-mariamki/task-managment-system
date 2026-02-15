import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management System"
    API_V1_STR: str = "/api/v1"
    
    # Datenbank-Konfiguration (SQLite für Entwicklung)
    # Wir verwenden eine lokale Datei 'sql_app.db' im Hauptverzeichnis
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"

    class Config:
        case_sensitive = True

settings = Settings()
