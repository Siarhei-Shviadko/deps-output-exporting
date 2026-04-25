from http import HTTPStatus
from json import JSONDecodeError

import requests
from msal import ConfidentialClientApplication

from deps_output_exporting.domain.model import ExternalStorageInfo, OneDriveCredentials

from ..exceptions import OneDriveError
from .abstract_storage import ExternalStorage

__all__ = ["OneDriveStorage"]


class OneDriveStorage(ExternalStorage):
    def __init__(self, scopes: list[str], base_url: str, authority_prefix: str):
        self._scopes = scopes
        self.base_url = base_url
        self.authority_prefix = authority_prefix

    def upload(self, file_name: str, output_file: bytes, storage_info: ExternalStorageInfo) -> None:
        credentials = storage_info.credentials

        app = self._create_app(credentials)
        access_token = self._get_token(app)

        endpoint = self._build_endpoint(
            user_id=credentials.user_id,
            path=storage_info.output_directory_path,
            file_name=file_name,
        )

        self._upload(endpoint, access_token, output_file)

    def _create_app(self, credentials: OneDriveCredentials) -> ConfidentialClientApplication:
        return ConfidentialClientApplication(
            client_id=credentials.client_id,
            client_credential=credentials.secret,
            authority=f"{self.authority_prefix}/{credentials.tenant_id}",
        )

    def _get_token(self, app: ConfidentialClientApplication) -> str:
        token = app.acquire_token_for_client(scopes=self._scopes)

        if (access_token := token.get("access_token")) is not None:
            return access_token

        error, error_description = token.get("error"), token.get("error_description")
        raise RuntimeError(f"There is no access token in response. Error: {error}, description: {error_description}")

    def _build_endpoint(self, user_id: str, path: str, file_name: str) -> str:
        return f"{self.base_url}/users/{user_id}/drive/root:/{path}/{file_name}:/content"

    def _upload(self, endpoint: str, access_token: str, output_file: bytes) -> None:
        upload_response = requests.put(
            endpoint,
            headers={"Authorization": "Bearer " + access_token},  # noqa: WPS336
            data=output_file,
        )

        if upload_response.status_code != HTTPStatus.CREATED:
            try:
                error_msg = upload_response.json().get("error")
            except JSONDecodeError:
                error_msg = upload_response.text
            raise OneDriveError(f"Error occurred during file uploading: {error_msg}")
