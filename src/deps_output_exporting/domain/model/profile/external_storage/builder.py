from typing import Optional, Union

from .code import Code
from .credentials import OneDriveCredentials, SalesforceCredentials
from .external_storage import ExternalStorageInfo
from .raw_data import CredentialsData

__all__ = ["ExternalStorageInfoBuilder"]


class ExternalStorageInfoBuilder:
    def __init__(self, code: Code) -> None:
        self._code: Code = code
        self._credentials: Optional[Union[OneDriveCredentials, SalesforceCredentials]] = None
        self._output_directory_path: Optional[str] = None

    @classmethod
    def with_code(cls, code: Code) -> "ExternalStorageInfoBuilder":
        return cls(code=code)

    def with_output_directory_path(self, output_directory_path: Optional[str] = None) -> "ExternalStorageInfoBuilder":
        if self._output_directory_path is not None:
            raise RuntimeError("Output directory path is already defined")

        self._output_directory_path = output_directory_path
        return self

    def with_credentials(self, credentials: CredentialsData) -> "ExternalStorageInfoBuilder":
        if self._credentials is not None:
            raise RuntimeError("Credentials are already defined")

        if self._code == Code.SALESFORCE:
            self._credentials = SalesforceCredentials(**credentials)
        elif self._code == Code.ONE_DRIVE:
            self._credentials = OneDriveCredentials(**credentials)

        return self

    def build(self) -> ExternalStorageInfo:
        return ExternalStorageInfo(  # type: ignore
            code=self._code,
            credentials=self._credentials,
            output_directory_path=self._output_directory_path,
        )
