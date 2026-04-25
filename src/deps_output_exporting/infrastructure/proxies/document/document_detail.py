from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = ["DocumentDetail"]


@dataclass
class DocumentDetail:
    title: str
    date: datetime
    engine: Optional[str]
