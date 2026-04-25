from dataclasses import dataclass
from typing import Optional

from ...shared import FieldType

__all__ = ["DocTypeField", "DocumentType"]


@dataclass
class DocTypeField:
    name: str
    code: str
    type: FieldType
    header_row: Optional[list[str]] = None
    base_type: Optional[FieldType] = None


@dataclass
class DocumentType:
    name: str
    fields: list[DocTypeField]
    engine: Optional[str]
