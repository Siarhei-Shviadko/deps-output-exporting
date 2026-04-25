from dataclasses import dataclass

from deps_message_flow.commands.common import Command

__all__ = ["PerformExporting", "PerformExportingReply"]


@dataclass(slots=True)
class PerformExporting(Command):
    document_id: str
    document_type_id: str
    profile_ids: list[str] | None


@dataclass(slots=True)
class PerformExportingReply(Command):
    error_type: str | None = None
    error_message: str | None = None
