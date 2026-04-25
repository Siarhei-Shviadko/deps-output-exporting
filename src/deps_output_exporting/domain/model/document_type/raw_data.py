from typing import TypedDict

from ..profile import ProfileData

__all__ = ["DocumentTypeData"]


class DocumentTypeData(TypedDict, total=False):
    document_type_id: str
    tenant_id: str
