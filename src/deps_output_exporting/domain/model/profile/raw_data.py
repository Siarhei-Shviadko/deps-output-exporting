from datetime import datetime
from typing import TypedDict

__all__ = ["ProfileData"]

from .schemas import SchemaData


class ProfileData(TypedDict, total=False):
    name: str
    creation_date: datetime
    schema: SchemaData
