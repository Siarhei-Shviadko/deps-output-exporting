from dataclasses import dataclass
from datetime import datetime

__all__ = ["GeneralInfo"]


@dataclass
class GeneralInfo:
    title: str
    type: str
    uploaded_date: datetime
    fields_number: int
    engine: str

    @classmethod
    def from_document_and_type(
        cls,
        title: str,
        type_: str,
        uploaded_date: datetime,
        fields_number: int,
        engine: str,
    ) -> "GeneralInfo":
        return cls(
            title=title,
            type=type_,
            uploaded_date=uploaded_date,
            fields_number=fields_number,
            engine=engine,
        )
