from dataclasses import dataclass

__all__ = ["UnifiedData"]


@dataclass
class UnifiedData:
    id: str
    page: int
