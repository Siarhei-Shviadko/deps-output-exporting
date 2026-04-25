from deps_output_exporting.constants import DEFAULT_PROFILE_NAME

from ..profile import Format, SchemaData
from ..profile.builder import ProfileBuilder
from ..shared import EntityId, TenantId
from .document_type import DocumentType

__all__ = ["DocumentTypeFactory"]


class DocumentTypeFactory:
    @classmethod
    def create(cls, id_: str, tenant_id: str, *, create_default_profile: bool = True) -> DocumentType:
        if not create_default_profile:
            return DocumentType(
                id_=EntityId(id_),
                tenant_id=TenantId(tenant_id),
            )

        default_profile = (
            ProfileBuilder(name=DEFAULT_PROFILE_NAME, format_="excel")
            .with_schema(schema_data=SchemaData(fields=[], needs_validation_results=True))
            .build()
        )
        return DocumentType(
            id_=EntityId(id_),
            tenant_id=TenantId(tenant_id),
            profiles={default_profile.id(): default_profile},
        )
