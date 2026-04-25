from http import HTTPStatus
from typing import Optional

from requests import Response

from ...exceptions import ValidationError
from ..generic import GenericProxy
from .proxy_interface import IValidationProxy
from .validation_result import ValidationInfo
from .validation_serializer import SerializedValidationResult

__all__ = ["ValidationProxy"]


class ValidationProxy(IValidationProxy, GenericProxy):
    SERVICE_PREFIX = "api/validation/v1/results"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_validation_results(self, document_id: str) -> ValidationInfo:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_id}",
            timeout=self._timeout,
            verify=self._verify,
        )

        return self._handle_response(response)

    def _handle_response(self, response: Response) -> Optional[ValidationInfo]:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        elif response.status_code != HTTPStatus.OK:
            raise ValidationError(response)
        return SerializedValidationResult.model_validate(response.json()).to_model()
