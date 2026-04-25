from dataclasses import asdict, dataclass
from typing import Any

__all__ = ["LineElement", "Line", "Paragraph"]


@dataclass
class LineElement:
    content: str


@dataclass
class Line:
    content: str
    elements: list[LineElement]


@dataclass
class Paragraph:
    content: str
    lines: list[Line]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
