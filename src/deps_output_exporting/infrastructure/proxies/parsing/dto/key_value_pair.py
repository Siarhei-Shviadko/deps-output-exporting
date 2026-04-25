from dataclasses import dataclass
from typing import Optional

__all__ = ["KeyValuePair"]


@dataclass
class KeyValuePair:
    key_content: str
    value_content: Optional[str] = None
    confidence: Optional[float] = None

    def to_dict(self) -> dict[str, str]:
        return {self.key_content: self.value_content}
