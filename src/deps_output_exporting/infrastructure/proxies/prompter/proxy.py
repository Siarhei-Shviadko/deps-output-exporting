from ...exceptions import PrompterError
from ..generic import GenericProxy
from .kv_data import KeyValues
from .kv_serializer import SerializedKeyValues

__all__ = ["PrompterProxy"]


class PrompterProxy(GenericProxy):
    SERVICE_PREFIX = "api/prompter/v1/documents"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def get_key_values(
        self,
        document_id: str,
    ) -> KeyValues:
        response = self._session.get(
            f"{self._base_url}/{self.SERVICE_PREFIX}/{document_id}/key-values",
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise PrompterError(response.content)

        return SerializedKeyValues.model_validate(response.json()).to_model()
