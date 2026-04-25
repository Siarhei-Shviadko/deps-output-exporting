from dataclasses import dataclass

from deps_message_flow.events.common import DomainEvent

__all__ = ["DeleteFiles"]


@dataclass
class DeleteFiles(DomainEvent):
    file_paths: list[str]
