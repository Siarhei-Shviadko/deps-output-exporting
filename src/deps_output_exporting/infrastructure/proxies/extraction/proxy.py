from ...exceptions import ExtractedDataError
from ..generic import GenericProxy
from .dto import ExtractedField
from .serializers import SerializedExtractedData

__all__ = ["ExtractionProxy"]


class ExtractionProxy(GenericProxy):
    SERVICE_PREFIX = "api/extraction/v2/extracted-data"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_extracted_data(self, document_id: str) -> list[ExtractedField]:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_id}",
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise ExtractedDataError(response.content)

        return SerializedExtractedData.model_validate(response.json()).to_model()
