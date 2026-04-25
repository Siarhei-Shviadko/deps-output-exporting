from dataclasses import dataclass

from deps_message_flow.commands.common import Command

__all__ = ["BuildOutput", "BuildOutputReply"]


@dataclass(slots=True)
class BuildOutput(Command):
    document_id: str
    document_type_id: str
    profile_id: str
    output_id: str


@dataclass(slots=True)
class BuildOutputReply(Command):
    document_id: str
    blob_name: str | None
    error_type: str | None
    error_message: str | None
    output_id: str
