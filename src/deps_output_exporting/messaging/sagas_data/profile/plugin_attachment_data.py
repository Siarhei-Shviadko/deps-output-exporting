from typing import Any, Optional

from deps_message_flow.sagas.orchestration import SagaData

from deps_output_exporting.domain.model import SchemaData

__all__ = ["PluginAttachmentSagaData"]


class PluginAttachmentSagaData(SagaData):
    def __init__(
        self,
        tenant_id: str,
        name: str,
        format_: str,
        profile_id: str,
        schema_data: SchemaData | None,
        *,
        document_type_id: Optional[str] = None,
    ) -> None:
        super().__init__(entity_id=document_type_id)
        self.tenant_id = tenant_id
        self.name = name
        self.format = format_
        self.schema_data = schema_data
        self._profile_id: str = profile_id

    @property
    def document_type_id(self) -> str:
        return self.entity_id

    @document_type_id.setter
    def document_type_id(self, document_type_id: str) -> None:
        self.entity_id = document_type_id

    @property
    def output_plugin_command_channel(self) -> str:
        return f"{self.tenant_id}-{self.name}-{self.profile_id}"

    @property
    def profile_id(self) -> str:
        return self._profile_id

    @profile_id.setter
    def profile_id(self, profile_id: str) -> None:
        self._profile_id = profile_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_type_id": self.document_type_id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "format": self.format,
            "profile_id": self.profile_id,
            "schema_data": self.schema_data,
        }

    @classmethod
    def from_dict(cls, raw_data: dict[str, Any]) -> "PluginAttachmentSagaData":
        return cls(
            document_type_id=raw_data["document_type_id"],
            tenant_id=raw_data["tenant_id"],
            name=raw_data["name"],
            format_=raw_data["format"],
            profile_id=raw_data["profile_id"],
            schema_data=raw_data["schema_data"],
        )
