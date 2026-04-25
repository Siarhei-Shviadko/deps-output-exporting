from typing import Optional

from ..shared import EntityId, TenantId
from .output import Output
from .output_state import OutputState
from .profile_info import ProfileInfo
from .schema_type import SchemaType

__all__ = ["OutputBuilder"]


class OutputBuilder:
    def __init__(self, document_id: str) -> None:
        self._document_id: str = document_id

        self._tenant_id: Optional[TenantId] = None
        self._profile_info: Optional[ProfileInfo] = None
        self._file_path: Optional[str] = None

    @classmethod
    def for_document_id(cls, document_id: str) -> "OutputBuilder":
        return cls(document_id)

    def for_tenant(self, tenant_id: str) -> "OutputBuilder":
        self._tenant_id = TenantId(tenant_id)
        return self

    def with_profile_info(self, id_: EntityId, version: str, schema_type: SchemaType | None) -> "OutputBuilder":
        self._profile_info = ProfileInfo(id_=id_, version=version, schema_type=schema_type)
        return self

    def with_file_path(self, file_path: str) -> "OutputBuilder":
        self._file_path = file_path
        return self

    def without_file_path(self) -> "OutputBuilder":
        return self

    def build(self) -> Output:
        return Output(
            id_=EntityId(),
            tenant_id=self._tenant_id,
            profile_info=self._profile_info,
            document_id=self._document_id,
            state=OutputState.READY,
            file_path=self._file_path,
        )
