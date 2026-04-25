from deps_message_flow.sagas.orchestration import SagaData

__all__ = ["ProfileDeletionSagaData"]


class ProfileDeletionSagaData(SagaData):
    def __init__(
        self,
        document_type_id: str,
        tenant_id: str,
        profile_id: str,
    ) -> None:
        super().__init__(entity_id=document_type_id)
        self.tenant_id = tenant_id
        self.profile_id = profile_id

    def to_dict(self) -> dict[str, str]:
        return {
            "document_type_id": self.entity_id,
            "tenant_id": self.tenant_id,
            "profile_id": self.profile_id,
        }

    @classmethod
    def from_dict(cls, raw_data: dict[str, str]) -> "ProfileDeletionSagaData":
        return cls(
            document_type_id=raw_data["document_type_id"],
            tenant_id=raw_data["tenant_id"],
            profile_id=raw_data["profile_id"],
        )
