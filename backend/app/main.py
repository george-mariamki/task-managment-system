from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api_v1.api import apirouter
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.utils.storage import ensure_upload_dir


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan-Event für Datenbank-Initialisierung.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_upload_dir()
app.mount(
    settings.UPLOAD_PUBLIC_PREFIX,
    StaticFiles(directory=str(settings.upload_dir_abs)),
    name="uploads",
)

app.include_router(apirouter, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"message": "Welcome to Task Management System API, status running"}


@app.get("/health")
def healthcheck():
    return {"status": "ok"}

@app.get("/debug-settings")
def debug_settings():
    """
    Debug endpoint لعرض الإعدادات الحالية.
    لا تتركيه في production.
    """
    return {
        "APP_ENV": settings.APP_ENV,
        "PROJECT_NAME": settings.PROJECT_NAME,
        "API_V1_STR": settings.API_V1_STR,
        "SQLALCHEMY_DATABASE_URI": settings.SQLALCHEMY_DATABASE_URI,
        "CORS_ORIGINS": settings.CORS_ORIGINS,
        "UPLOAD_DIR": settings.UPLOAD_DIR,
        "UPLOAD_PUBLIC_PREFIX": settings.UPLOAD_PUBLIC_PREFIX,
        "UPLOAD_ALLOWED_EXTENSIONS": settings.UPLOAD_ALLOWED_EXTENSIONS,
        "UPLOAD_MAX_SIZE_BYTES": settings.UPLOAD_MAX_SIZE_BYTES,
        "ACCESS_TOKEN_EXPIRE_MINUTES": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        # لا نرجّع SECRET_KEY حفاظًا على الأمان
    }
