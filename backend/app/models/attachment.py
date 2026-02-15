from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Attachment(Base):
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)     # Originaler Dateiname (z.B. "bericht.pdf")
    file_path = Column(String, nullable=False)    # Pfad auf dem Server (z.B. "uploads/1_bericht.pdf")
    file_type = Column(String, nullable=True)     # MIME-Type (z.B. "application/pdf")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Fremdschlüssel zur Verknüpfung mit der Aufgabe
    task_id = Column(Integer, ForeignKey("task.id"), nullable=True) # Nullable, falls Datei erst hochgeladen wird
    
    # Beziehung zur Task-Entität
    task = relationship("Task", back_populates="attachments")
