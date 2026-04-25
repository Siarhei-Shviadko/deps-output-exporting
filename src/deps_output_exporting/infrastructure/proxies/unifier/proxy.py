from ...exceptions import UnifierError
from ..generic import GenericProxy
from .unified_data import UnifiedData
from .unifier_serializer import SerializedUnifiedData

__all__ = ["UnifierProxy"]


class UnifierProxy(GenericProxy):
    SERVICE_PREFIX = "api/unifier/v1/unified_data"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_unified_data(self, document_id: str) -> list[UnifiedData]:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_id}",
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise UnifierError(response.content)

        return SerializedUnifiedData.model_validate(response.json()).to_model()
