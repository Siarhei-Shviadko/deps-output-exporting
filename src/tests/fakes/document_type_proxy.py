from deps_output_exporting.infrastructure import DocumentType

__all__ = ["FakeDocumentTypeProxy"]


class FakeDocumentTypeProxy:
    def __init__(self) -> None:
        self.document_types: dict[str, DocumentType] = {}

    def get_document_type(self, document_type_id: str) -> DocumentType:
        return self.document_types[document_type_id]
