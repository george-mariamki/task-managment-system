from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Verknüpfung zum Besitzer (User)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="tasks")

    # Neue Beziehung: Eine Aufgabe hat viele Anhänge
    # cascade="all, delete-orphan" löscht Anhänge automatisch, wenn Task gelöscht wird
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")
