import json

import pytest

from deps_output_exporting.infrastructure.exceptions import SalesforceError
from tests.data import json_edata_output_some_fields


class TestSalesforceStorage:
    BASE_URL = "https://graph.microsoft.com/v1.0"

    def test_upload_file__success(
        self,
        salesforce_storage,
        external_storage_info__salesforce,
        generated_name_json,
        salesforce_access_token,
        salesforse_auth_success_request_mock,
        salesforse_upload_success_request_mock,
    ):
        expected_json_body = json.dumps(
            {
                "PathOnClient": generated_name_json,
                "OwnerId": external_storage_info__salesforce.credentials.owner_id,
                "FirstPublishLocationId": external_storage_info__salesforce.credentials.location_id,
            }
        ).encode("utf-8")
        expected_stream_body = json.dumps(json_edata_output_some_fields).encode("utf-8")

        salesforce_storage.upload(
            file_name=generated_name_json,
            output_file=json.dumps(json_edata_output_some_fields).encode("utf8"),
            storage_info=external_storage_info__salesforce,
        )

        upload_request = salesforse_upload_success_request_mock.last_request

        assert upload_request.headers["Authorization"] == f"Bearer {salesforce_access_token}"

        assert expected_json_body in upload_request.body
        assert expected_stream_body in upload_request.body

    def test_upload_file__error_auth_request(
        self,
        salesforce_storage,
        external_storage_info__salesforce,
        generated_name_json,
        salesforse_auth_error_request_mock,
    ):
        with pytest.raises(SalesforceError) as error:
            salesforce_storage.upload(
                file_name=generated_name_json,
                output_file=json.dumps(json_edata_output_some_fields).encode("utf8"),
                storage_info=external_storage_info__salesforce,
            )

        assert error.value.args[0] == f"Error occurred during authentication: invalid_client_id"

    def test_upload_file__error_upload_request(
        self,
        salesforce_storage,
        external_storage_info__salesforce,
        generated_name_json,
        salesforse_auth_success_request_mock,
        salesforse_upload_error_request_mock,
    ):
        with pytest.raises(SalesforceError) as error:
            salesforce_storage.upload(
                file_name=generated_name_json,
                output_file=json.dumps(json_edata_output_some_fields).encode("utf8"),
                storage_info=external_storage_info__salesforce,
            )

        assert (
            error.value.args[0]
            == "Error occurred during file uploading: Required fields are missing: [Title], The argument is null or invalid."
        )
