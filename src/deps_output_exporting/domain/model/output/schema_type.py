from enum import Enum

__all__ = ["SchemaType"]


class SchemaType(str, Enum):
    EXTRACTED_DATA = "extracted_data"
    DOCUMENT_LAYOUT = "document_layout"
