from typing import Any

from deps_output_exporting.domain.model import (
    DocumentLayoutSchema,
    ExtractedDataSchema,
    ParsingFeature,
    ParsingType,
    Schema,
)

__all__ = ["SchemaMapper"]


class SchemaMapper:
    @staticmethod
    def from_dict(raw_schema: dict[str, Any]) -> Schema:
        if raw_schema.get("features") is not None:
            return DocumentLayoutSchema(
                parsing_type=ParsingType(raw_schema["parsing_type"]),
                features=[ParsingFeature(feature) for feature in raw_schema["features"]],
            )
        elif raw_schema.get("fields") is not None and raw_schema.get("needs_validation_results") is not None:
            return ExtractedDataSchema(
                fields=raw_schema["fields"],
                needs_validation_results=raw_schema["needs_validation_results"],
            )

    @staticmethod
    def to_dict(schema: Schema) -> dict[str, Any]:
        if isinstance(schema, DocumentLayoutSchema):
            return {
                "parsing_type": schema.parsing_type.value,
                "features": [feature.value for feature in schema.features],
            }

        elif isinstance(schema, ExtractedDataSchema):
            return {"fields": schema.fields, "needs_validation_results": schema.needs_validation_results}

        raise RuntimeError(f"Unexpected schema {schema} gotten")
