from typing import Any, Optional

from deps_message_flow.sagas.orchestration import SagaData

from deps_output_exporting.domain.model import (
    EntityId,
    ExternalStorageInfoData,
    Format,
    SchemaData,
)

__all__ = ["ProfileCreationSagaData"]


class ProfileCreationSagaData(SagaData):
    def __init__(
        self,
        document_type_id: str,
        tenant_id: str,
        name: str,
        schema: SchemaData,
        format_: str,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
        *,
        profile_id: Optional[EntityId] = None,
    ) -> None:
        super().__init__(entity_id=document_type_id)
        self.tenant_id = tenant_id
        self.name = name
        self.schema = schema
        self.format = format_
        self.external_storages_info = external_storages_info

        self._profile_id = profile_id

    @property
    def routing_info_command_channel(self) -> str:
        return f"{self.name}-{self.tenant_id}"

    @property
    def profile_id(self) -> Optional[EntityId]:
        return self._profile_id

    @profile_id.setter
    def profile_id(self, value: Optional[EntityId]) -> None:
        self._profile_id = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_type_id": self.entity_id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "schema": self.schema,
            "format": self.format,
            "external_storages_info": self.external_storages_info,
            "profile_id": self.profile_id() if self.profile_id is not None else None,
        }

    @classmethod
    def from_dict(cls, raw_data: dict[str, Any]) -> "ProfileCreationSagaData":
        return cls(
            document_type_id=raw_data["document_type_id"],
            tenant_id=raw_data["tenant_id"],
            name=raw_data["name"],
            schema=raw_data["schema"],
            format_=raw_data["format"],
            external_storages_info=raw_data["external_storages_info"],
            profile_id=EntityId(raw_data["profile_id"]) if raw_data["profile_id"] else None,
        )
