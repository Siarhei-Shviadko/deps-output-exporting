from abc import ABC, abstractmethod

from .validation_result import ValidationInfo

__all__ = ["IValidationProxy"]


class IValidationProxy(ABC):
    @abstractmethod
    def get_validation_results(self, document_id: str) -> ValidationInfo:  # noqa: WPS463
        pass
