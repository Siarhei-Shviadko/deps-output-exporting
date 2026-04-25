from ...exceptions import DocumentTypeError
from ..generic import GenericProxy
from .dto import DocumentType
from .serializers import SerializedDocumentType

__all__ = ["DocumentTypeProxy"]


class DocumentTypeProxy(GenericProxy):
    SERVICE_PREFIX = "api/document-type/v1/types"
    V2_SERVICE_PREFIX = SERVICE_PREFIX.replace("v1", "v2")

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_document_type(self, document_type_id: str) -> DocumentType:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_type_id}",
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise DocumentTypeError(response.content)

        return SerializedDocumentType.model_validate(response.json()).to_model()

    def get_or_create_document_type(self, name: str) -> str:
        response = self._session.get(
            f"{self._base_url}/{self.V2_SERVICE_PREFIX}/{name}",
        )
        if not response.ok:
            raise DocumentTypeError(response.content)

        return response.json()["id"]
