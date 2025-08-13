from typing import TypeVar

from src.database import Base
from pydantic import BaseModel

DBModelType = TypeVar('DBModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class DataMapper:
    db_model: DBModelType = None
    schema: SchemaType = None

    @classmethod
    def map_to_domain_entity(cls, data) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data) -> DBModelType:
        return cls.db_model(**data.model_dump())
