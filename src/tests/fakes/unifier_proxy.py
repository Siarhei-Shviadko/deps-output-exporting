from deps_output_exporting.infrastructure import UnifiedData

__all__ = ["FakeUnifierProxy"]


class FakeUnifierProxy:
    def __init__(self) -> None:
        self.unified_data: dict[str, list[UnifiedData]] = {}

    def get_unified_data(self, document_id: str) -> list[UnifiedData]:
        return self.unified_data[document_id]
