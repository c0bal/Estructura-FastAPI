from typing import List, Optional, Type, TypeVar, Any, Dict
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import re
from log import get_logger

ORMModel = TypeVar("ORMModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

log = get_logger(__name__)


def _parse_integrity_error(error: IntegrityError) -> str:
    msg = str(error.orig).lower()

    if "duplicate key value violates unique constraint" in msg:
        match = re.search(r'\((?P<field>.*?)\)=\((?P<value>.*?)\)', msg)
        if match:
            field = match.group("field").replace("_", " ")
            value = match.group("value")
            return f"A record with {field}: '{value}' already exists."
        return "A record with duplicate values already exists."

    if "violates foreign key constraint" in msg:
        col_match = re.search(r"key \((?P<column>.*?)\)=\((?P<value>.*?)\)", msg)
        if col_match:
            column = col_match.group("column").replace("_", " ")
            return f"The value of field '{column}' does not match any existing record."

        return "Invalid reference to another table. Please verify related data exists."

    # Generic case
    return "Database integrity error."


class CRUDRepository:
    def __init__(self, model: Type[ORMModel], m2m_fields: Optional[Dict[str, Any]] = None):
        self._model = model
        self._name = model.__name__
        self._m2m_fields = m2m_fields or {}

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ORMModel]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).first()

    def get_many(self, db: Session, *args, skip: int = 0, limit: int = 1000, **kwargs) -> List[ORMModel]:
        return (
            db.query(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_create: CreateSchemaType) -> ORMModel:
        if not isinstance(obj_create, BaseModel):
            raise HTTPException(
                status_code=400,
                detail="Expected a Pydantic object, but received a dictionary."
            )

        try:
            obj_data = obj_create.model_dump(exclude_unset=True)
            m2m_data = {
                field: [db.get(model_class, i) for i in obj_data.pop(field, [])]
                for field, model_class in self._m2m_fields.items()
            }

            db_obj = self._model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            for field, rel_objs in m2m_data.items():
                setattr(db_obj, field.replace("_ids", ""), rel_objs)

            db.commit()
            db.refresh(db_obj)
            return db_obj

        except IntegrityError as e:
            db.rollback()
            log.error("Integrity error while creating %s: %s", self._name, str(e))
            raise HTTPException(status_code=400, detail=_parse_integrity_error(e))

        except Exception as e:
            db.rollback()
            log.exception("Unexpected error while creating %s:", self._name)
            raise HTTPException(status_code=500, detail="Unexpected error while creating the record.")

    def update(self, db: Session, db_obj: ORMModel, obj_update: UpdateSchemaType) -> ORMModel:
        try:
            obj_data = obj_update.model_dump(exclude_unset=True)
            obj_data = {key: value for key, value in obj_data.items() if value is not None}

            for field, value in obj_data.items():
                setattr(db_obj, field, value)

            m2m_data = {}
            for field, model_class in self._m2m_fields.items():
                ids = obj_data.pop(field, [])
                if not ids:
                    m2m_data[field] = []
                else:
                    ids = [id for id in ids if id is not None]
                    m2m_data[field] = [db.get(model_class, i) for i in ids]

            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            for field, rel_objs in m2m_data.items():
                setattr(db_obj, field.replace("_ids", ""), rel_objs)

            db.commit()
            db.refresh(db_obj)
            return db_obj

        except IntegrityError as e:
            db.rollback()
            log.error("Integrity error while updating %s: %s", self._name, str(e))
            raise HTTPException(status_code=400, detail=_parse_integrity_error(e))

        except Exception as e:
            db.rollback()
            log.exception("Unexpected error while updating %s:", self._name)
            raise HTTPException(status_code=500, detail="Unexpected error while updating the record.")

    def delete(self, db: Session, db_obj: ORMModel) -> ORMModel:
        try:
            for field in self._m2m_fields.keys():
                rel_field = field.replace("_ids", "")
                if hasattr(db_obj, rel_field):
                    getattr(db_obj, rel_field).clear()
            db.commit()

            db.delete(db_obj)
            db.commit()
            return db_obj

        except IntegrityError as e:
            db.rollback()
            log.error("Integrity error while deleting %s: %s", self._name, str(e))
            raise HTTPException(status_code=400, detail=_parse_integrity_error(e))

        except Exception as e:
            db.rollback()
            log.exception("Unexpected error while deleting %s:", self._name)
            raise HTTPException(status_code=500, detail="Unexpected error while deleting the record.")
