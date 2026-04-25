from deps_output_exporting.infrastructure.proxies.document.document_detail import (
    DocumentDetail,
)

__all__ = ["FakeDocumentProxy"]


class FakeDocumentProxy:
    def __init__(self) -> None:
        self.document_details: dict[str, DocumentDetail] = {}

    def get_document_detail(self, document_id: str) -> DocumentDetail:
        return self.document_details[document_id]
