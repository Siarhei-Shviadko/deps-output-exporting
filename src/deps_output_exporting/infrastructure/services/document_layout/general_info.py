from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = ["GeneralInfo"]


@dataclass
class GeneralInfo:
    title: str
    type: str
    uploaded_date: datetime
    pages_number: int
    engine: Optional[str] = None

    @classmethod
    def from_document_and_type(
        cls,
        title: str,
        type_: str,
        uploaded_date: datetime,
        pages_number: int,
        engine: Optional[str] = None,
    ) -> "GeneralInfo":
        return cls(
            title=title,
            type=type_,
            uploaded_date=uploaded_date,
            pages_number=pages_number,
            engine=engine,
        )
