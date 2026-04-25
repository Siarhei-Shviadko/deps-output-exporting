from typing import Any

from sqlalchemy import JSON, and_, delete, func, literal, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.sql import Delete, Join, Select
from sqlalchemy.sql.functions import Function

from ...tables import document_type_table, profile_table

__all__ = ["DocumentTypeQueryFactory"]


class DocumentTypeQueryFactory:
    def __init__(self) -> None:
        self._document_type_table = document_type_table
        self._profile_table = profile_table

    @property
    def joined_tables(self) -> Join:
        return self._document_type_table.join(
            self._profile_table,
            self._document_type_table.c.id == self._profile_table.c.document_type_id,
            isouter=True,
        )

    @property
    def aggregated_profiles(self) -> Function:
        return func.json_agg(
            func.json_build_object(
                "id",
                self._profile_table.c.id,
                "document_type_id",
                self._profile_table.c.document_type_id,
                "name",
                self._profile_table.c.name,
                "creation_date",
                self._profile_table.c.creation_date,
                "schema",
                self._profile_table.c.schema,
                "version",
                self._profile_table.c.version,
                "format",
                self._profile_table.c.format,
                "external_storages_info",
                self._profile_table.c.external_storages_info,
                "exporting_type",
                self._profile_table.c.exporting_type,
            ),
        )

    def select_document_type(self, document_type_id: str, tenant_id: str) -> Select:
        return (
            select(
                self._document_type_table.c.id,
                self._document_type_table.c.tenant_id,
                self.aggregated_profiles.label("profiles"),
            )
            .select_from(self.joined_tables)
            .group_by(self._document_type_table.c.id, self._document_type_table.c.tenant_id)
            .where(
                and_(
                    self._document_type_table.c.id == document_type_id,
                    self._document_type_table.c.tenant_id == tenant_id,
                ),
            )
        )

    def insert_document_type(self) -> Insert:
        return insert(self._document_type_table).on_conflict_do_nothing()

    def insert_document_type_returning_id(self, raw_doc_types: list[dict[str, Any]]) -> Insert:
        return (
            insert(self._document_type_table)
            .values(raw_doc_types)
            .on_conflict_do_nothing()
            .returning(self._document_type_table.c.id)
        )

    def insert_profiles(self) -> Insert:
        return insert(self._profile_table).on_conflict_do_nothing()

    def delete_document_type(self, document_type_id: str, tenant_id: str) -> Delete:
        return delete(self._document_type_table).where(
            and_(
                self._document_type_table.c.id == document_type_id,
                self._document_type_table.c.tenant_id == tenant_id,
            ),
        )
