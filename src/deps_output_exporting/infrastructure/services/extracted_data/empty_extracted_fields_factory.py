from typing import Union

from deps_output_exporting.infrastructure import (
    DocTypeField,
    ExtractedField,
    FieldType,
    GenericData,
    KeyValuePairData,
)

ListData = Union[list[GenericData], list[KeyValuePairData]]


class EmptyExtractedFieldsFactory:
    def __init__(self, dt_field: DocTypeField) -> None:
        self._dt_field = dt_field

        self._type_to_factory_mapping = {
            FieldType.CHECKMARK: self._empty_generic_data,
            FieldType.STRING: self._empty_generic_data,
            FieldType.ENUM: self._empty_generic_data,
            FieldType.DATE: self._empty_generic_data,
            FieldType.LIST: self._empty_list_data,
            FieldType.DICT: self._empty_kv_pair_data,
        }

    @classmethod
    def for_document_type_field(cls, dt_field: DocTypeField) -> "EmptyExtractedFieldsFactory":
        return cls(dt_field)

    def supports_this_type(self) -> bool:
        if self._dt_field.base_type is None:
            return self._dt_field.type in self._type_to_factory_mapping

        return (
            self._dt_field.type in self._type_to_factory_mapping
            and self._dt_field.base_type in self._type_to_factory_mapping
        )

    def make_empty_extracted_field(self) -> ExtractedField:
        empty_data = self._type_to_factory_mapping[self._dt_field.type]()

        return ExtractedField(
            code=self._dt_field.code,
            name=self._dt_field.name,
            type=self._dt_field.type,
            base_type=self._dt_field.base_type,
            data=empty_data,
        )

    def _empty_generic_data(self) -> GenericData:
        return GenericData(
            value=None,
            confidence=None,
            source_id=None,
        )

    def _empty_list_data(self) -> ListData:
        return [self._type_to_factory_mapping[self._dt_field.base_type]()]

    def _empty_kv_pair_data(self) -> KeyValuePairData:
        return KeyValuePairData(
            key=self._empty_generic_data(),
            value=self._empty_generic_data(),
        )
