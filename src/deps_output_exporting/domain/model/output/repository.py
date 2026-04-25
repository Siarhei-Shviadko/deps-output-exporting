from typing import Optional, Protocol

from ..output import Output

__all__ = ["IOutputRepository"]


class IOutputRepository(Protocol):
    def save(self, output: Output) -> None:
        ...

    def find_by_id(self, tenant_id: str, output_id: str) -> Optional[Output]:
        ...

    def find_by_document_id(self, tenant_id: str, document_id: str) -> list[Output]:
        ...

    def delete(self, tenant_id: str, document_id: str, output_id: str) -> Optional[Output]:
        ...

    def delete_all(self, tenant_id: str, output_ids: list[str]) -> None:
        ...

    def delete_outdated_outputs(self, document_id: str, tenant_id: str, profile_id: str) -> list[Output]:
        ...
