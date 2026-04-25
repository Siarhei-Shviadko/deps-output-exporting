from sqlalchemy import and_, delete, desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.sql import Delete, Select

from ...tables import routing_info_table

__all__ = ["RoutingInfoQueryFactory"]


class RoutingInfoQueryFactory:
    def __init__(self) -> None:
        self._routing_info_table = routing_info_table

    def insert_routing_info(self) -> Insert:
        insert_query = insert(self._routing_info_table)
        return insert_query.on_conflict_do_update(
            index_elements=[
                self._routing_info_table.c.tenant_id,
                self._routing_info_table.c.document_type_id,
                self._routing_info_table.c.profile_id,
            ],
            set_={"command_channel": insert_query.excluded.command_channel},
        )

    def find_routing_info(self, tenant_id: str, document_type_id: str, profile_id: str) -> Select:
        return select(self._routing_info_table).where(
            and_(
                self._routing_info_table.c.tenant_id == tenant_id,
                self._routing_info_table.c.document_type_id == document_type_id,
                self._routing_info_table.c.profile_id == profile_id,
            ),
        )

    def delete_routing_info(self, tenant_id: str, document_type_id: str, profile_id: str) -> Delete:
        return (
            delete(self._routing_info_table)
            .where(
                and_(
                    self._routing_info_table.c.tenant_id == tenant_id,
                    self._routing_info_table.c.document_type_id == document_type_id,
                    self._routing_info_table.c.profile_id == profile_id,
                ),
            )
            .returning(self._routing_info_table)
        )
