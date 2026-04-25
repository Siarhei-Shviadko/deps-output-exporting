from deps_output_exporting.extras.storage import FileStorageRequestError

from .generic import GenericProxy

__all__ = ["FileStorageProxy"]


class FileStorageProxy(GenericProxy):
    SERVICE_PREFIX = "api/storage/v1/file"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool):
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

    def upload_file(self, file_path: str, file_name: str, output_file: bytes) -> str:
        response = self._session.post(
            self._get_url(file_path),
            files={"file": (file_name, output_file)},
            data={"replaceIfExists": True},
            timeout=self._timeout,
            verify=self._verify,
        )
        if not response.ok:
            raise FileStorageRequestError(response.content)

        return response.json()["path"]

    def _get_url(self, file_path: str) -> str:
        return f"{self._base_url}/{self.SERVICE_PREFIX}/{file_path}"
