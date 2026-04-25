from datetime import date
from typing import Optional, Union

from pydantic import Field

from deps_output_exporting.domain.model import (
    DocumentLayoutSchema,
    ExtractedDataSchema,
    Format,
    Profile,
)

from ..base import ConfiguredBaseModel
from ..schemas import SerializedDocumentLayoutSchema, SerializedExtractedDataSchema
from .external_storage import (
    GetExternalStorageInfoResponse,
    SerializedExternalStorageInfo,
)

__all__ = [
    "SaveProfileRequest",
    "SaveProfileResponse",
    "ProfilesListResponse",
    "ProfileResponse",
    "CreateProfileRequest",
]


class SaveProfileRequest(ConfiguredBaseModel):
    name: str
    schema_: Union[SerializedExtractedDataSchema, SerializedDocumentLayoutSchema, None] = Field(  # noqa: WPS120
        alias="schema",
    )
    external_storages_info: Optional[list[SerializedExternalStorageInfo]] = None


class CreateProfileRequest(ConfiguredBaseModel):
    name: str
    schema_: Union[SerializedExtractedDataSchema, SerializedDocumentLayoutSchema, None] = Field(  # noqa: WPS120
        alias="schema",
    )
    format: str
    external_storages_info: Optional[list[SerializedExternalStorageInfo]] = None


class SaveProfileResponse(ConfiguredBaseModel):
    id: str


class ProfileResponse(ConfiguredBaseModel):
    id: str
    name: str
    creation_date: date
    schema_: Union[SerializedExtractedDataSchema, SerializedDocumentLayoutSchema, None] = Field(  # noqa: WPS120
        alias="schema",
    )
    version: str
    format: str
    external_storages_info: Optional[list[GetExternalStorageInfoResponse]]
    exporting_type: str = Field(alias="exportingType")

    @classmethod
    def from_model(cls, profile: Profile) -> "ProfileResponse":
        if profile.schema is None:
            schema = None
        elif isinstance(profile.schema, DocumentLayoutSchema):
            schema = SerializedDocumentLayoutSchema.from_model(profile.schema)
        elif isinstance(profile.schema, ExtractedDataSchema):
            schema = SerializedExtractedDataSchema.from_model(profile.schema)
        else:
            raise RuntimeError("Unknown schema data obtained")

        external_storages_info = [
            GetExternalStorageInfoResponse.from_model(external_storage_info)
            for external_storage_info in profile.external_storages_info or []
        ]

        return cls(
            id=profile.id(),
            name=profile.name,
            creation_date=profile.creation_date.date(),
            schema_=schema,
            version=profile.version,
            format=profile.format(),
            external_storages_info=external_storages_info,
            exporting_type=profile.exporting_type,
        )


class ProfilesListResponse(ConfiguredBaseModel):
    profiles: list[ProfileResponse]
