from datetime import datetime, timezone
from typing import Optional

from ..shared import EntityId, Guard, ImmutableCheck, TenantId
from .output_state import OutputState
from .profile_info import ProfileInfo

__all__ = ["Output"]


class Output:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())
    profile_info = Guard[ProfileInfo](ProfileInfo, ImmutableCheck())
    document_id = Guard[str](str, ImmutableCheck())
    state = Guard[OutputState](OutputState, ImmutableCheck())
    file_path = Guard[str](str, ImmutableCheck())
    creation_date = Guard[datetime](datetime, ImmutableCheck())

    def __init__(
        self,
        id_: EntityId,
        tenant_id: TenantId,
        profile_info: ProfileInfo,
        document_id: str,
        state: OutputState,
        file_path: str | None,
        creation_date: Optional[datetime] = None,
    ):
        self.id = id_
        self.tenant_id = tenant_id
        self.profile_info = profile_info
        self.document_id = document_id
        self.state = state
        self.creation_date = creation_date or datetime.now(timezone.utc)

        if file_path:
            self.file_path = file_path

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def assign_file(self, file_path: str | None) -> None:
        if file_path:
            self.file_path = file_path
