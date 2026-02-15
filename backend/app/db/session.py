from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Engine erstellen
# check_same_thread=False ist nur für SQLite notwendig
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}
)

# SessionLocal Klasse erstellen
# Diese Klasse wird verwendet, um Datenbank-Sitzungen für jede Anfrage zu erstellen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
