import base64
from http import HTTPStatus
from json import JSONDecodeError, dumps

import requests

from deps_output_exporting.domain.model import (
    ExternalStorageInfo,
    SalesforceCredentials,
)

from ..exceptions import SalesforceError
from .abstract_storage import ExternalStorage

__all__ = ["SalesforceStorage"]


class SalesforceStorage(ExternalStorage):
    def __init__(self, base_url: str, auth_endpoint: str, upload_endpoint: str):
        self.base_url = base_url
        self.auth_endpoint = auth_endpoint
        self.upload_endpoint = upload_endpoint

    def upload(self, file_name: str, output_file: bytes, storage_info: ExternalStorageInfo) -> None:
        credentials = storage_info.credentials

        access_token = self._get_access_token(credentials.basic_token)
        self._upload_file(access_token, file_name, output_file, credentials)

    def _get_access_token(self, basic_token: str) -> str:
        auth_response = self._make_auth_request(basic_token)

        if auth_response.status_code != HTTPStatus.OK:
            try:
                auth_error = auth_response.json().get("error")
            except JSONDecodeError:
                auth_error = auth_response.text
            raise SalesforceError(f"Error occurred during authentication: {auth_error}")

        return auth_response.json()["access_token"]

    def _make_auth_request(self, basic_token: str) -> requests.Response:
        return requests.post(
            url="".join([self.base_url, self.auth_endpoint]),
            data={"grant_type": "client_credentials"},
            headers=self._create_auth_header("Basic", basic_token),
        )

    def _upload_file(
        self,
        access_token: str,
        file_name: str,
        output_file: bytes,
        credentials: SalesforceCredentials,
    ) -> None:
        upload_body = self._create_upload_body(file_name, credentials.owner_id, credentials.location_id)

        upload_response = self._make_upload_request(access_token, file_name, output_file, upload_body)

        if upload_response.status_code != HTTPStatus.CREATED:
            try:
                upload_error = ", ".join([error.get("message") for error in upload_response.json()])
            except JSONDecodeError:
                upload_error = upload_response.text
            raise SalesforceError(f"Error occurred during file uploading: {upload_error}")

    def _make_upload_request(
        self,
        access_token: str,
        file_name: str,
        output_file: bytes,
        upload_body: dict[str, str],
    ) -> requests.Response:
        return requests.post(
            url="".join([self.base_url, self.upload_endpoint]),
            files={  # type: ignore
                "json": (None, dumps(upload_body), "application/json"),
                "VersionData": (file_name, output_file, "application/octet-stream"),
            },
            headers=self._create_auth_header("Bearer", access_token),
        )

    def _create_upload_body(self, file_name: str, owner_id: str, location_id: str) -> dict[str, str]:
        return {
            "PathOnClient": file_name,
            "OwnerId": owner_id,
            "FirstPublishLocationId": location_id,
        }

    @staticmethod
    def _create_auth_header(prefix: str, token: str) -> dict[str, str]:
        return {"Authorization": " ".join([prefix, token])}
