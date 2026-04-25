from deps_output_exporting.domain.model import ExtractedDataSchema, SchemaData

from ..base import ConfiguredBaseModel

__all__ = ["SerializedExtractedDataSchema"]


class SerializedExtractedDataSchema(ConfiguredBaseModel):
    fields: list[str]
    needs_validation_results: bool

    @classmethod
    def from_model(cls, schema: ExtractedDataSchema) -> "SerializedExtractedDataSchema":
        return cls(
            fields=schema.fields,
            needs_validation_results=schema.needs_validation_results,
        )

    def to_dto(self) -> SchemaData:
        return {"fields": self.fields, "needs_validation_results": self.needs_validation_results}
