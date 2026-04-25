from deps_output_exporting.infrastructure import ExtractedField

__all__ = ["FakeExtractionProxy"]


class FakeExtractionProxy:
    def __init__(self) -> None:
        self.extracted_data: dict[str, list[ExtractedField]] = {}

    def get_extracted_data(self, document_id: str) -> list[ExtractedField]:
        return self.extracted_data[document_id]
