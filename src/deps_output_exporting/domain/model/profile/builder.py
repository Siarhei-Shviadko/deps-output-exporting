from datetime import datetime
from typing import Optional

from ..profile import ExportingType, Format, Profile, Schema, SchemaData
from ..shared import EntityId
from .external_storage import ExternalStorageInfoData, ExternalStorageInfoFactory

__all__ = ["ProfileBuilder"]


class ProfileBuilder:
    def __init__(
        self,
        name: str,
        format_: str,
        creation_date: Optional[datetime] = None,
        version: Optional[str] = None,
    ) -> None:
        self._id = EntityId()
        self._name: str = name
        self._format: Format = Format(format_)
        self._creation_date = creation_date
        self._version: Optional[str] = version
        self._schema: Optional[Schema] = None
        self._external_storages_info: Optional[list] = None
        self._exporting_type: ExportingType = ExportingType.BUILT_IN

    def with_id(self, id_: str) -> "ProfileBuilder":
        self._id = EntityId(id_)
        return self

    def as_plugin(self) -> "ProfileBuilder":
        self._exporting_type = ExportingType.PLUGIN
        return self

    def as_builtin(self) -> "ProfileBuilder":
        self._exporting_type = ExportingType.BUILT_IN
        return self

    def with_schema(self, schema_data: SchemaData) -> "ProfileBuilder":
        self._schema = Profile.create_schema(schema_data)
        return self

    def with_external_storages_info(
        self,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> "ProfileBuilder":
        if external_storages_info is None:
            return self

        self._external_storages_info = ExternalStorageInfoFactory.create_external_storages_info(external_storages_info)
        return self

    def build(self) -> Profile:
        return Profile(
            id_=self._id,
            name=self._name,
            creation_date=self._creation_date,
            version=self._version,
            format_=self._format,
            schema=self._schema,
            external_storages_info=self._external_storages_info,
            exporting_type=self._exporting_type,
        )
