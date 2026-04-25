from sqlalchemy import and_, delete, desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.sql import Delete, Select

from ...tables import output_table

__all__ = ["OutputQueryFactory"]


class OutputQueryFactory:
    def __init__(self) -> None:
        self._output_table = output_table

    def insert_output(self) -> Insert:
        insert_query = insert(self._output_table)
        return insert_query.on_conflict_do_update(
            index_elements=[self._output_table.c.id],
            set_=dict(insert_query.excluded),
        )

    def select_output(self, tenant_id: str, output_id: str) -> Select:
        return select(self._output_table).where(
            and_(
                self._output_table.c.id == output_id,
                self._output_table.c.tenant_id == tenant_id,
            ),
        )

    def select_outputs(self, tenant_id: str, document_id: str) -> Select:
        return select(self._output_table).where(
            and_(
                self._output_table.c.tenant_id == tenant_id,
                self._output_table.c.document_id == document_id,
            ),
        )

    def delete_output(self, tenant_id: str, document_id: str, output_id: str) -> Delete:
        return (
            delete(self._output_table)
            .where(
                and_(
                    self._output_table.c.tenant_id == tenant_id,
                    self._output_table.c.document_id == document_id,
                    self._output_table.c.id == output_id,
                ),
            )
            .returning(self._output_table)
        )

    def delete_output_batch(self, tenant_id: str, output_ids: list[str]) -> Delete:
        return delete(self._output_table).where(
            and_(
                self._output_table.c.tenant_id == tenant_id,
                self._output_table.c.id.in_(output_ids),
            ),
        )

    def delete_outdated_outputs(self, document_id: str, tenant_id: str, profile_id: str) -> Delete:
        select_old_outputs = (
            select(self._output_table.c.id)
            .where(
                and_(
                    self._output_table.c.tenant_id == tenant_id,
                    self._output_table.c.document_id == document_id,
                    self._output_table.c.profile_info["id"].astext == profile_id,
                ),
            )
            .order_by(desc(self._output_table.c.creation_date))
            .offset(1)
        )

        return (
            delete(self._output_table)
            .where(self._output_table.c.id.in_(select_old_outputs))
            .returning(self._output_table)
        )
