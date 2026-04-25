import json
from uuid import uuid4

import pytest

from deps_output_exporting.infrastructure.exceptions import OneDriveError
from deps_output_exporting.infrastructure.external_storages import OneDriveStorage
from tests.data import json_edata_output_some_fields


class TestOneDriveStorage:
    BASE_URL = "https://graph.microsoft.com/v1.0"

    def test_upload_file__success(
        self,
        onedrive_storage,
        external_storage_info__onedrive,
        generated_name_json,
        put_onedrive_success_request_mock,
        mocker,
    ):
        mocker.patch.object(OneDriveStorage, "_create_app")
        token = mocker.patch.object(OneDriveStorage, "_get_token", return_value=uuid4().hex)

        onedrive_storage.upload(
            file_name=generated_name_json,
            output_file=json.dumps(json_edata_output_some_fields).encode("utf8"),
            storage_info=external_storage_info__onedrive,
        )

        token.assert_called_once()

        request = put_onedrive_success_request_mock.last_request
        assert (
            request.url
            == f"{self.BASE_URL}/users/{external_storage_info__onedrive.credentials.user_id}/drive/root:/{external_storage_info__onedrive.output_directory_path}/{generated_name_json}:/content"
        )
        assert request.headers["Authorization"] == f"Bearer {token.return_value}"
        assert request.body == json.dumps(json_edata_output_some_fields).encode("utf8")

    def test_upload_file__token_error(
        self,
        onedrive_storage,
        external_storage_info__onedrive,
        generated_name_json,
        put_onedrive_success_request_mock,
        mocker,
    ):
        with pytest.raises(RuntimeError):
            mocker.patch.object(OneDriveStorage, "_create_app")
            token = mocker.patch.object(OneDriveStorage, "_get_token", side_effect=RuntimeError)

            onedrive_storage.upload(
                file_name=generated_name_json,
                output_file=json.dumps(json_edata_output_some_fields).encode("utf8"),
                storage_info=external_storage_info__onedrive,
            )

    def test_upload_file__error_in_response(
        self,
        onedrive_storage,
        external_storage_info__onedrive,
        generated_name_json,
        put_onedrive_error_request_mock,
        mocker,
    ):
        mocker.patch.object(OneDriveStorage, "_create_app")
        mocker.patch.object(OneDriveStorage, "_get_token", return_value=uuid4().hex)

        with pytest.raises(OneDriveError) as error:
            onedrive_storage.upload(
                file_name=generated_name_json,
                output_file=json.dumps(json_edata_output_some_fields).encode("utf8"),
                storage_info=external_storage_info__onedrive,
            )

        assert (
            error.value.args[0]
            == "Error occurred during file uploading: {'code': 'error_code', 'message': 'Error message'}"
        )
