from typing import Any

from sqlalchemy import Row

from deps_output_exporting.domain.model import DocumentType, EntityId, TenantId

from .profile import ProfileMapper

__all__ = ["DocumentTypeMapper"]


class DocumentTypeMapper:
    @staticmethod
    def from_row(raw_doc_type: Row) -> DocumentType:
        profiles = [ProfileMapper.from_dict(profile) for profile in raw_doc_type.profiles]
        return DocumentType(
            id_=EntityId(raw_doc_type.id),
            tenant_id=TenantId(raw_doc_type.tenant_id),
            profiles={profile.id.value: profile for profile in profiles},
        )

    @staticmethod
    def to_dict(document_type: DocumentType) -> dict[str, Any]:
        profiles = [
            ProfileMapper.to_dict(profile, document_type.id.value) for profile in document_type.profiles.values() or []
        ]
        return {
            "id": document_type.id(),
            "tenant_id": document_type.tenant_id(),
            "profiles": profiles,
        }
