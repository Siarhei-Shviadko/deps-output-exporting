from ..shared import EntityId, Guard, ImmutableCheck, TenantId

__all__ = ["RoutingInfo"]


class RoutingInfo:
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())
    document_type_id = Guard[EntityId](EntityId, ImmutableCheck())
    profile_id = Guard[EntityId](EntityId, ImmutableCheck())
    command_channel = Guard[str](str, ImmutableCheck())

    def __init__(
        self,
        tenant_id: TenantId,
        document_type_id: EntityId,
        profile_id: EntityId,
        command_channel: str,
    ):
        self.tenant_id = tenant_id
        self.document_type_id = document_type_id
        self.profile_id = profile_id
        self.command_channel = command_channel

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.tenant_id == other.tenant_id
            and self.document_type_id == other.document_type_id
            and self.profile_id == other.profile_id
        )

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.tenant_id = },",
                f"{self.document_type_id = },",
                f"{self.profile_id = },",
                f"{self.command_channel = }>",
            ),
        )
