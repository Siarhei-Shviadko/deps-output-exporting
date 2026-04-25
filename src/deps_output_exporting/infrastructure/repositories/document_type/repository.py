from typing import Any, Optional

from sqlalchemy.engine.base import Connection

from deps_output_exporting.domain.model import DocumentType, IDocumentTypeRepository
from deps_output_exporting.extras.datasource import Database

from .mappers import DocumentTypeBatchMapper, DocumentTypeMapper
from .query_factory import DocumentTypeQueryFactory

__all__ = ["DocumentTypeRepository"]


class DocumentTypeRepository(IDocumentTypeRepository):
    def __init__(self, database: Database) -> None:
        self.db = database
        self._query_factory = DocumentTypeQueryFactory()

    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        with self.db.connection() as conn:
            document_type = conn.execute(
                self._query_factory.select_document_type(document_type_id, tenant_id),
            ).fetchone()
        if document_type:
            return DocumentTypeMapper.from_row(document_type)

        return None

    def delete(self, document_type_id: str, tenant_id: str) -> None:
        with self.db.connection() as conn:
            self._delete_document_type(conn, document_type_id, tenant_id)

    def save(self, document_type: DocumentType) -> None:
        raw_doc_type = DocumentTypeMapper.to_dict(document_type)
        with self.db.connection() as conn:
            self._save_full_document_type(conn, raw_doc_type)

    def update(self, document_type: DocumentType) -> None:
        raw_doc_type = DocumentTypeMapper.to_dict(document_type)
        with self.db.connection() as conn:
            self._delete_document_type(conn, document_type.id(), document_type.tenant_id())
            self._save_full_document_type(conn, raw_doc_type)

    def save_all(self, document_types: list[DocumentType]) -> None:
        raw_document_type_batch, raw_profiles = DocumentTypeBatchMapper.to_dicts(
            document_types,
        )
        with self.db.connection() as conn:
            saved_doc_types = self._save_document_type_batch(conn, raw_document_type_batch)
            profiles_to_save = list(
                filter(lambda profile: (profile["document_type_id"],) in saved_doc_types, raw_profiles),
            )
            if profiles_to_save:
                self._save_profiles(conn, profiles_to_save)

    def _save_full_document_type(self, conn: Connection, raw_doc_type: dict[str, Any]) -> None:
        self._save_document_type(conn, raw_doc_type["id"], raw_doc_type["tenant_id"])
        self._save_profiles(conn, raw_doc_type["profiles"])

    def _save_document_type(self, conn: Connection, document_type_id: str, tenant_id: str) -> None:
        conn.execute(
            self._query_factory.insert_document_type(),
            parameters={"id": document_type_id, "tenant_id": tenant_id},
        )

    def _save_profiles(self, conn: Connection, raw_profiles: list[dict[str, Any]]) -> None:
        conn.execute(self._query_factory.insert_profiles(), raw_profiles)

    def _save_document_type_batch(self, conn: Connection, raw_doc_types: list[dict[str, Any]]) -> list[tuple[str]]:
        return conn.execute(self._query_factory.insert_document_type_returning_id(raw_doc_types)).fetchall()

    def _delete_document_type(self, conn: Connection, document_type_id: str, tenant_id: str) -> None:
        conn.execute(self._query_factory.delete_document_type(document_type_id, tenant_id))
