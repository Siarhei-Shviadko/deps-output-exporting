from unittest import mock

import pytest
from deps_message_flow.sagas.testing_support import *

from deps_output_exporting.domain.exceptions import (
    DocumentTypeNotFound,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import IDocumentTypeRepository
from deps_output_exporting.messaging.sagas import ProfileCreationSaga
from deps_output_exporting.messaging.sagas_data import ProfileCreationSagaData


@pytest.mark.profile_creation_saga
def test_profile_creation_saga(
    profile_name,
    extracted_data_schema_data,
    profile_format,
    external_storages_info_schema_data,
    profile_creation_steps,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type,
):
    fake_document_type_repository.save(document_type=document_type)

    profile_creation_saga_data = ProfileCreationSagaData(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
        name=profile_name,
        schema=extracted_data_schema_data,
        format_=profile_format(),
        external_storages_info=external_storages_info_schema_data,
    )

    suts = (
        SagaUnitTestSupport.given()
        .saga(
            ProfileCreationSaga(steps=profile_creation_steps),
            profile_creation_saga_data,
        )
        .expect_completed_successfully()
    )
    saga_data = suts.saga_data

    assert saga_data["tenant_id"] == document_type.tenant_id()
    assert saga_data["document_type_id"] == document_type.id()
    assert saga_data["name"] == profile_name
    assert saga_data["schema"] == extracted_data_schema_data
    assert saga_data["format"] == profile_format()
    assert saga_data["external_storages_info"] == external_storages_info_schema_data


@pytest.mark.profile_creation_saga
def test_profile_creation_saga_document_type_not_exist_failed(
    document_type_id,
    test_tenant_id,
    profile_name,
    extracted_data_schema_data,
    profile_format,
    external_storages_info_schema_data,
    profile_creation_steps,
):
    profile_creation_saga_data = ProfileCreationSagaData(
        document_type_id=document_type_id,
        tenant_id=test_tenant_id,
        name=profile_name,
        schema=extracted_data_schema_data,
        format_=profile_format(),
        external_storages_info=external_storages_info_schema_data,
    )
    expected_exception = DocumentTypeNotFound(document_type_id)
    profile_creation_steps.create_profile = mock.Mock(side_effect=expected_exception)
    (
        SagaUnitTestSupport.given()
        .saga(
            ProfileCreationSaga(steps=profile_creation_steps),
            profile_creation_saga_data,
        )
        .expect_exception(expected_exception)
    )


@pytest.mark.profile_creation_saga
def test_profile_creation_saga_failed(
    document_type_id,
    test_tenant_id,
    profile_name,
    extracted_data_schema_data,
    profile_format,
    external_storages_info_schema_data,
    profile_creation_steps,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type,
    profile_id,
):
    fake_document_type_repository.save(document_type=document_type)
    profile_creation_saga_data = ProfileCreationSagaData(
        document_type_id=document_type_id,
        tenant_id=test_tenant_id,
        name=profile_name,
        schema=extracted_data_schema_data,
        format_=profile_format(),
        external_storages_info=external_storages_info_schema_data,
    )
    expected_exception = RuntimeError(profile_id)
    profile_creation_steps.create_routing_info = mock.Mock(side_effect=expected_exception)
    (
        SagaUnitTestSupport.given()
        .saga(
            ProfileCreationSaga(steps=profile_creation_steps),
            profile_creation_saga_data,
        )
        .expect_rolled_back()
    )
