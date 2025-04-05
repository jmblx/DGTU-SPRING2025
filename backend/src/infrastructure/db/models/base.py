from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, registry

mapper_registry = registry(metadata=MetaData())


class Base(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __abstract__ = True
