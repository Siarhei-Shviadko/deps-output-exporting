from datetime import datetime, timezone
from typing import Generic, Optional
from uuid import uuid4

from deps_output_exporting.constants import DEFAULT_PROFILE_NAME

from ..shared import EntityId, Guard, ImmutableCheck
from .external_storage import (
    ExternalStorageInfo,
    ExternalStorageInfoData,
    ExternalStorageInfoFactory,
)
from .format import Format
from .schemas import (
    DocumentLayoutSchema,
    ExportingType,
    ExtractedDataSchema,
    Schema,
    SchemaData,
)

__all__ = ["Profile"]


class Profile(Generic[Schema]):
    id = Guard[EntityId](EntityId, ImmutableCheck())
    name = Guard[str](str, ImmutableCheck())
    creation_date = Guard[datetime](datetime, ImmutableCheck())
    schema = Guard[Schema](Schema, ImmutableCheck())  # type: ignore
    version = Guard[str](str, ImmutableCheck())
    format = Guard[Format](Format, ImmutableCheck())
    external_storages_info = Guard[list[ExternalStorageInfo]](list)
    exporting_type = Guard[ExportingType](ExportingType, ImmutableCheck())

    def __init__(
        self,
        name: str,
        format_: Format,
        exporting_type: ExportingType,
        *,
        id_: Optional[EntityId] = None,
        schema: Optional[Schema] = None,
        creation_date: Optional[datetime] = None,
        version: Optional[str] = None,
        external_storages_info: Optional[list[ExternalStorageInfo]] = None,
    ):
        self.id = id_ or EntityId()
        self.creation_date = creation_date or datetime.now(timezone.utc)
        self.name = name
        self.version = version or uuid4().hex
        self.format = format_
        self.exporting_type = exporting_type
        if schema:
            self.schema = schema

        if external_storages_info is not None:
            self.external_storages_info = external_storages_info

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.id = },",
                f"{self.creation_date = },",
                f"{self.name = },",
                f"{self.schema = },",
                f"{self.version = },",
                f"{self.format = }>",
            ),
        )

    def update(
        self,
        name: str,
        schema: SchemaData,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> None:
        self._name = name
        self._schema = self.create_schema(schema)  # type: ignore
        self._version = uuid4().hex
        if external_storages_info is not None:
            self._external_storages_info = ExternalStorageInfoFactory.create_external_storages_info(
                external_storages_info,
            )

    @staticmethod
    def create_schema(schema_data: SchemaData) -> Schema:
        keys_to_schema_mapper = {
            ("parsing_type", "features"): DocumentLayoutSchema,
            ("fields", "needs_validation_results"): ExtractedDataSchema,
        }
        schema_dict_keys = set(schema_data)

        for keys, schema_class in keys_to_schema_mapper.items():
            if schema_dict_keys.issuperset(keys):
                return schema_class(**schema_data)
        raise RuntimeError(f"Can not build profile schema with {schema_dict_keys}")

    def is_updatable(self) -> bool:
        return self.exporting_type == ExportingType.PLUGIN

    def is_default(self) -> bool:
        return self.name == DEFAULT_PROFILE_NAME
