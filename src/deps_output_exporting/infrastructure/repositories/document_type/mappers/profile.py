import logging
from typing import Any

from dateutil import parser

from deps_output_exporting.domain.model import EntityId, ExportingType, Format, Profile

from .external_storage_info import ExternalStorageInfoMapper
from .schema import SchemaMapper

__all__ = ["ProfileMapper"]

logger = logging.getLogger()


class ProfileMapper:
    @staticmethod
    def from_dict(raw_profile: dict[str, Any]) -> Profile:
        if "external_storages_info" in raw_profile:
            external_storages_info = [
                ExternalStorageInfoMapper.from_dict(external_storage_info)
                for external_storage_info in raw_profile["external_storages_info"] or []  # noqa: WPS529
            ]
        else:
            external_storages_info = None

        return Profile(
            id_=EntityId(raw_profile["id"]),
            name=raw_profile["name"],
            creation_date=parser.isoparse(raw_profile["creation_date"]),
            schema=(SchemaMapper.from_dict(schema_data) if (schema_data := raw_profile["schema"]) else None),
            version=raw_profile["version"],
            format_=Format(raw_profile["format"]),
            external_storages_info=external_storages_info,
            exporting_type=ExportingType(raw_profile["exporting_type"]),
        )

    @staticmethod
    def to_dict(profile: Profile, document_type_id: str) -> dict[str, Any]:
        if profile.external_storages_info is not None:
            external_storages_info = [
                ExternalStorageInfoMapper.to_dict(external_storage_info)
                for external_storage_info in profile.external_storages_info
            ]
        else:
            external_storages_info = None

        return {
            "id": profile.id(),
            "name": profile.name,
            "creation_date": profile.creation_date,
            "schema": (sc := profile.schema) and SchemaMapper.to_dict(sc),
            "version": profile.version,
            "document_type_id": document_type_id,
            "format": profile.format(),
            "external_storages_info": external_storages_info,
            "exporting_type": profile.exporting_type,
        }
