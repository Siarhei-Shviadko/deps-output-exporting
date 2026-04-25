from typing import Optional

from deps_output_exporting.domain.model import IOutputRepository, Output
from deps_output_exporting.extras.datasource import Database

from .mappers import OutputMapper
from .query_factory import OutputQueryFactory

__all__ = ["OutputRepository"]


class OutputRepository(IOutputRepository):
    def __init__(self, database: Database) -> None:
        self.db = database
        self._query_factory = OutputQueryFactory()

    def save(self, output: Output) -> None:
        raw_output = OutputMapper.to_dict(output)
        with self.db.connection() as conn:
            conn.execute(self._query_factory.insert_output(), raw_output)

    def find_by_id(self, tenant_id: str, output_id: str) -> Optional[Output]:
        with self.db.connection() as conn:
            output = conn.execute(
                self._query_factory.select_output(tenant_id=tenant_id, output_id=output_id),
            ).fetchone()
        return OutputMapper.from_row(output) if output else None

    def find_by_document_id(self, tenant_id: str, document_id: str) -> list[Output]:
        with self.db.connection() as conn:
            outputs = conn.execute(
                self._query_factory.select_outputs(tenant_id, document_id),
            ).fetchall()
        return [OutputMapper.from_row(output) for output in outputs]

    def delete(self, tenant_id: str, document_id: str, output_id: str) -> Optional[Output]:
        with self.db.connection() as conn:
            deleted_output = conn.execute(
                self._query_factory.delete_output(tenant_id, document_id, output_id),
            ).fetchone()
        return OutputMapper.from_row(deleted_output) if deleted_output else None

    def delete_all(self, tenant_id: str, output_ids: list[str]) -> None:
        with self.db.connection() as conn:
            conn.execute(self._query_factory.delete_output_batch(tenant_id, output_ids))

    def delete_outdated_outputs(self, document_id: str, tenant_id: str, profile_id: str) -> list[Output]:
        with self.db.connection() as conn:
            deleted_outputs = conn.execute(
                self._query_factory.delete_outdated_outputs(document_id, tenant_id, profile_id),
            )
        return [OutputMapper.from_row(output) for output in deleted_outputs]
