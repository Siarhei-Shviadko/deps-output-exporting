from datetime import datetime
from typing import Optional

from ..base_serializer import ConfiguredBaseModel
from .document_detail import DocumentDetail

__all__ = ["SerializedDocumentDetail"]


class SerializedDocumentDetail(ConfiguredBaseModel):
    title: str
    date: datetime
    engine: Optional[str]

    def to_model(self) -> DocumentDetail:
        return DocumentDetail(
            title=self.title,
            date=self.date,
            engine=self.engine,
        )
