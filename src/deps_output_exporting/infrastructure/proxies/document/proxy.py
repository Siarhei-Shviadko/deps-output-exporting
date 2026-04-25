from ...exceptions import DocumentError
from ..generic import GenericProxy
from .document_detail import DocumentDetail
from .document_serializer import SerializedDocumentDetail

__all__ = ["DocumentProxy"]


class DocumentProxy(GenericProxy):
    SERVICE_PREFIX = "api/document/v1/documents"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_document_detail(self, document_id: str) -> DocumentDetail:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_id}",
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise DocumentError(response.content)

        return SerializedDocumentDetail.model_validate(response.json()).to_model()
