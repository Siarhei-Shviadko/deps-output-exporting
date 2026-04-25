from typing import Optional, Union

from pydantic import field_validator

from ...base_serializer import ConfiguredBaseModel
from ...shared import FieldType
from ..dto import DocTypeField, DocumentType

__all__ = ["SerializedDocumentType"]


class ColumnMeta(ConfiguredBaseModel):
    title: str


class TableFieldMeta(ConfiguredBaseModel):
    columns: list[ColumnMeta]


class ListFieldMeta(ConfiguredBaseModel):
    base_type: str
    base_type_meta: Optional[TableFieldMeta]

    @field_validator("base_type_meta", mode="before")
    @classmethod
    def table_or_list_meta(cls, base_type_meta):  # noqa: N805
        if base_type_meta and "columns" in base_type_meta:
            return base_type_meta
        return None


class SerializedTypeField(ConfiguredBaseModel):
    name: str
    code: str
    field_type: FieldType
    field_meta: Union[TableFieldMeta, ListFieldMeta, None]

    @field_validator("field_meta", mode="before")
    @classmethod
    def table_or_list_meta(cls, field_meta):  # noqa: N805
        if field_meta and (field_meta.get("columns") or field_meta.get("baseType")):
            return field_meta
        return None

    def to_model(self) -> DocTypeField:
        header_row = None
        base_type = None
        if isinstance(self.field_meta, TableFieldMeta):
            header_row = [col.title for col in self.field_meta.columns]
        elif isinstance(self.field_meta, ListFieldMeta):
            header_row = (
                [col.title for col in self.field_meta.base_type_meta.columns]
                if self.field_meta.base_type == FieldType.TABLE.value
                else None
            )
            base_type = FieldType(self.field_meta.base_type)

        return DocTypeField(
            name=self.name,
            code=self.code,
            type=self.field_type,
            header_row=header_row,
            base_type=base_type,
        )


class SerializedDocumentType(ConfiguredBaseModel):
    fields: list[SerializedTypeField]
    document_type: str
    engine: Optional[str]

    def to_model(self) -> DocumentType:
        return DocumentType(
            name=self.document_type,
            engine=self.engine,
            fields=[field.to_model() for field in self.fields],
        )
