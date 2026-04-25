import json

import pytest

from deps_output_exporting.messaging import ErrorType
from deps_output_exporting.messaging.handlers import build_output_handler
from tests.fakes import (
    FakeFileStorageProxy,
    FakeOutputRepository,
    FakeSalesforceStorage,
)


@pytest.mark.build_output_nosave
@pytest.mark.usefixtures(
    "save_doc_type_two_types_of_profile_with_external_storages_info",
    "fake_document_proxy_with_document_detail",
    "fake_extraction_proxy_with_extracted_data",
    "fake_document_type_proxy_with_document_type",
    "fake_unifier_proxy_with_unify_data",
    "fake_validation_proxy_with_validation_info",
)
def test_build_output__ok(
    build_output_message,
    fake_file_storage_proxy: FakeFileStorageProxy,
    fake_salesforce_storage: FakeSalesforceStorage,
    fake_output_repository: FakeOutputRepository,
    test_tenant_id,
    document_id,
    output_id,
):
    [command] = build_output_handler(build_output_message)

    assert fake_file_storage_proxy.storage
    assert fake_salesforce_storage.storage
    payload = json.loads(command.payload)
    assert payload["document_id"] == document_id
    assert payload["output_id"] == output_id
    assert payload["blob_name"]
    assert payload["error_type"] is None
    assert payload["error_message"] is None


@pytest.mark.build_output_nosave
def test_build_output__business_error(build_output_message):
    [command] = build_output_handler(build_output_message)

    payload = json.loads(command.payload)
    assert payload["error_type"] == ErrorType.BUSINESS
    assert payload["error_message"]
    assert payload["blob_name"] is None


@pytest.mark.build_output_nosave
@pytest.mark.usefixtures(
    "save_doc_type_two_types_of_profile_with_external_storages_info",
    "fake_document_proxy",
)
def test_build_output__sistem_error(build_output_message):
    [command] = build_output_handler(build_output_message)

    payload = json.loads(command.payload)
    assert payload["error_type"] == ErrorType.SYSTEM
    assert payload["error_message"]
    assert payload["blob_name"] is None
