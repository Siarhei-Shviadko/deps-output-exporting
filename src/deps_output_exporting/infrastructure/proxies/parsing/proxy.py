from deps_output_exporting.domain.model import ParsingFeature, ParsingType

from ...exceptions import ParsingError
from ..generic import GenericProxy
from .dto import DocumentLayout
from .serializers import SerializedDocumentLayout

__all__ = ["ParsingProxy"]


class ParsingProxy(GenericProxy):
    SERVICE_PREFIX = "api/parsing/v1/document-layout"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_document_layout(
        self,
        document_id: str,
        parsing_type: ParsingType,
        features: list[ParsingFeature],
    ) -> DocumentLayout:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_id}",
            params={"parsingType": parsing_type, "features": features},
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise ParsingError(response.content)

        return SerializedDocumentLayout.model_validate(response.json()).to_model()
