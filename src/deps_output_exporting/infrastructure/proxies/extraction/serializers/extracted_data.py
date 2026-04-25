from typing import Union

from ...base_serializer import ConfiguredBaseModel
from ..dto import ExtractedField
from .field_data import (
    SerializedGenericData,
    SerializedKeyValueFieldData,
    SerializedTableFieldData,
)

__all__ = ["SerializedExtractedData"]

SerializedFieldData = Union[
    SerializedTableFieldData,
    SerializedKeyValueFieldData,
    SerializedGenericData,
    list[SerializedTableFieldData],
    list[SerializedKeyValueFieldData],
    list[SerializedGenericData],
]


class SerializedExtractedField(ConfiguredBaseModel):
    field_code: str
    data: SerializedFieldData

    def to_model(self) -> ExtractedField:
        if isinstance(self.data, list):
            data = [data.to_model() for data in self.data]
        else:
            data = self.data.to_model()  # type: ignore
        return ExtractedField(
            code=self.field_code,
            data=data,  # type: ignore
        )


class SerializedExtractedData(ConfiguredBaseModel):
    fields: list[SerializedExtractedField]

    def to_model(self) -> list[ExtractedField]:
        return [field.to_model() for field in self.fields]
