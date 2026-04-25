from dataclasses import dataclass

from deps_message_flow.events.common import DomainEvent

__all__ = ["DocumentTypeCreated", "DocumentTypeDeleted", "DocumentTypeChanged"]


@dataclass
class DocumentTypeCreated(DomainEvent):
    document_type: str
    tenant: str


@dataclass
class DocumentTypeDeleted(DomainEvent):
    document_type: str
    tenant: str


@dataclass
class DocumentTypeChanged(DomainEvent):
    document_id: str
