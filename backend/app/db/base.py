# Importieren aller Modelle für Alembic (Datenbank-Migrationen)
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.task import Task  # noqa
from app.models.attachment import Attachment  # noqa