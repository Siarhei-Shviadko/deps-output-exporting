from typing import Optional

from deps_output_exporting.domain.model import IRoutingInfoRepository, RoutingInfo
from deps_output_exporting.extras.datasource import Database

from .mappers import RoutingInfoMapper
from .query_factory import RoutingInfoQueryFactory

__all__ = ["RoutingInfoRepository"]


class RoutingInfoRepository(IRoutingInfoRepository):
    def __init__(self, database: Database) -> None:
        self.db = database
        self._query_factory = RoutingInfoQueryFactory()

    def save(self, routing_info: RoutingInfo) -> None:
        raw_routing_info = RoutingInfoMapper.to_dict(routing_info)
        with self.db.connection() as conn:
            conn.execute(self._query_factory.insert_routing_info(), raw_routing_info)

    def find(self, tenant_id: str, document_type_id: str, profile_id: str) -> Optional[RoutingInfo]:
        with self.db.connection() as conn:
            routing_info = conn.execute(
                self._query_factory.find_routing_info(tenant_id, document_type_id, profile_id),
            ).fetchone()
        return RoutingInfoMapper.from_row(routing_info) if routing_info else None

    def delete(self, tenant_id: str, document_type_id: str, profile_id: str) -> Optional[RoutingInfo]:
        with self.db.connection() as conn:
            deleted_routing_info = conn.execute(
                self._query_factory.delete_routing_info(tenant_id, document_type_id, profile_id),
            ).fetchone()
        return RoutingInfoMapper.from_row(deleted_routing_info) if deleted_routing_info else None
