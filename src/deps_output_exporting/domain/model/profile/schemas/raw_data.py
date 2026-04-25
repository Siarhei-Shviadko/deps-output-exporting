from typing import TypedDict, TypeVar

from .document_layout import DocumentLayoutSchema
from .extracted_data import ExtractedDataSchema
from .parsing_feature import ParsingFeature
from .parsing_type import ParsingType

__all__ = ["SchemaData", "Schema"]

Schema = TypeVar("Schema", DocumentLayoutSchema, ExtractedDataSchema)


class SchemaData(TypedDict, total=False):
    parsing_type: ParsingType
    features: list[ParsingFeature]
    fields: list[str]
    needs_validation_results: bool
