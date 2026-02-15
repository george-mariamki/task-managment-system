from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Tabellennamen automatisch aus dem Klassennamen generieren
    # z.B. User -> user, TaskItem -> task_item
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
