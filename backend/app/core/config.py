import os
import json
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


def _env_files() -> List[str]:
    app_env = os.getenv("APP_ENV", "development").lower().strip()

    files = [str(BASE_DIR / ".env")]

    if app_env == "development":
        files.append(str(BASE_DIR / ".env.development"))
    elif app_env == "production":
        files.append(str(BASE_DIR / ".env.production"))
    elif app_env == "test":
        files.append(str(BASE_DIR / ".env.test"))

    return files


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=_env_files(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = Field(default="development")

    PROJECT_NAME: str = Field(default="Task Management System")
    API_V1_STR: str = Field(default="/api/v1")

    SECRET_KEY: str = Field(default="CHANGETHISINPRODUCTIONSUPERSECRETKEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 8)

    SQLALCHEMY_DATABASE_URI: str = Field(default="sqlite:///./sql_app.db")

    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )

    UPLOAD_DIR: str = Field(default="uploads")
    UPLOAD_PUBLIC_PREFIX: str = Field(default="/uploads")
    UPLOAD_ALLOWED_EXTENSIONS: List[str] = Field(
        default_factory=lambda: [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".doc", ".docx"]
    )
    UPLOAD_MAX_SIZE_MB: int = Field(default=5)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("["):
                return json.loads(s)
            return [item.strip() for item in s.split(",") if item.strip()]
        return v

    @field_validator("UPLOAD_ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def _parse_upload_extensions(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return [str(x).lower().strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("["):
                raw = json.loads(s)
                return [str(x).lower().strip() for x in raw if str(x).strip()]
            return [item.lower().strip() for item in s.split(",") if item.strip()]
        return v

    @property
    def upload_dir_abs(self) -> Path:
        return (BASE_DIR / self.UPLOAD_DIR).resolve()


settings = Settings()
