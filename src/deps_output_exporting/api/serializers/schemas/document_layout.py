from deps_output_exporting.domain.model import (
    DocumentLayoutSchema,
    ParsingFeature,
    ParsingType,
    SchemaData,
)

from ..base import ConfiguredBaseModel

__all__ = ["SerializedDocumentLayoutSchema"]


class SerializedDocumentLayoutSchema(ConfiguredBaseModel):
    parsing_type: ParsingType
    features: list[ParsingFeature]

    @classmethod
    def from_model(cls, schema: DocumentLayoutSchema) -> "SerializedDocumentLayoutSchema":
        return cls(parsing_type=schema.parsing_type, features=schema.features)

    def to_dto(self) -> SchemaData:
        return {"parsing_type": self.parsing_type, "features": self.features}
