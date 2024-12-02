from typing import Any, Dict, Type
from datetime import datetime, timezone

from sqlalchemy import MetaData, Column, Integer, DateTime
from sqlalchemy.orm import as_declarative, declared_attr

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

class_registry: Dict[str, Any] = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: Any
    __name__: str
    __abstract__: bool = True
    metadata = metadata

    # Auto-generar __tablename__ si no está definido
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Clave primaria por defecto
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Timestamps con zona horaria
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
        nullable=False,
    )
