from dataclasses import dataclass
from typing import TypedDict

from deps_message_flow.commands.common import Command

__all__ = ["GetDocumentTypesReply", "GetDocumentTypes"]


class GetDocumentTypes(Command):
    pass  # noqa: WPS604, WPS420


class DocumentType(TypedDict):
    document_type_id: str
    tenant_id: str


@dataclass
class GetDocumentTypesReply(Command):
    document_types: list[DocumentType]
