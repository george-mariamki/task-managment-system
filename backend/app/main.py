from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Lifespan-Event für Datenbank-Initialisierung
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Erstellt alle Tabellen beim Start
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan  # Hier binden wir das Event
)

# CORS-Konfiguration (Erlaubt Anfragen von bestimmten Quellen)
origins = [
    "http://localhost:5173", # Frontend-URL (Vite)
    "http://127.0.0.1:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Erlaubte Quellen 
    allow_credentials=True,
    allow_methods=["*"],   # Alle Methoden erlauben (GET, POST, usw)
    allow_headers=["*"],   # Alle Header erlauben
)

# Mount the uploads directory to be accessible at /uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Router einbinden
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Management System API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
