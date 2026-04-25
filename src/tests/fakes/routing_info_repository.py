from typing import Optional

from deps_output_exporting.domain.model import IRoutingInfoRepository, RoutingInfo

__all__ = ["FakeRoutingInfoRepository"]


class FakeRoutingInfoRepository(IRoutingInfoRepository):
    def __init__(self, fake_db: Optional[dict[tuple[str, str, str], RoutingInfo]] = None) -> None:
        self._routing_info_db = {} if fake_db is None else fake_db

    def __repr__(self) -> str:
        return str(self._routing_info_db)

    def find(self, tenant_id: str, document_type_id: str, profile_id: str) -> Optional[RoutingInfo]:
        routing_info_key = (tenant_id, document_type_id, profile_id)
        return self._routing_info_db.get(routing_info_key)

    def save(self, routing_info: RoutingInfo) -> None:
        routing_info_key = (routing_info.tenant_id(), routing_info.document_type_id(), routing_info.profile_id())
        self._routing_info_db[routing_info_key] = routing_info

    def delete(self, tenant_id: str, document_type_id: str, profile_id: str) -> None:
        routing_info_key = (tenant_id, document_type_id, profile_id)
        self._routing_info_db.pop(routing_info_key, None)
