from deps_output_exporting.infrastructure import ValidationInfo

__all__ = ["FakeValidationProxy"]


class FakeValidationProxy:
    def __init__(self) -> None:
        self.validation_info: dict[str, ValidationInfo] = {}

    def get_validation_results(self, document_id: str) -> ValidationInfo:
        return self.validation_info[document_id]
