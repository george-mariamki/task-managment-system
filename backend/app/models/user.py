from sqlalchemy import Boolean, Column, Integer, String
from app.db.base_class import Base

class User(Base):
    # Primärschlüssel und Indexierung für schnelle Abfragen
    id = Column(Integer, primary_key=True, index=True)
    
    # E-Mail muss einzigartig sein
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Passwort wird gehasht gespeichert, niemals im Klartext
    hashed_password = Column(String, nullable=False)
    
    # Status des Benutzers (aktiv/inaktiv)
    is_active = Column(Boolean, default=True)
    
    # Admin-Rechte für zukünftige Erweiterungen
    is_superuser = Column(Boolean, default=False)
