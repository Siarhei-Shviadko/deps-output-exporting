from unittest import mock

import pytest
from deps_message_flow.sagas.testing_support import *

from deps_output_exporting.domain.exceptions import DocumentTypeNotFound
from deps_output_exporting.domain.model import IDocumentTypeRepository
from deps_output_exporting.messaging.sagas import ProfileDeletionSaga
from deps_output_exporting.messaging.sagas_data import ProfileDeletionSagaData


@pytest.mark.profile_deletion_saga
def test_profile_deletion_saga(
    profile_deletion_steps,
    fake_document_type_repository: IDocumentTypeRepository,
    doc_type_two_types_of_profile,
    profile_extracted_data_schema,
):
    fake_document_type_repository.save(document_type=doc_type_two_types_of_profile)
    profile_id = profile_extracted_data_schema.id()
    document_type_id = doc_type_two_types_of_profile.id()
    tenant_id = doc_type_two_types_of_profile.tenant_id()

    profile_deletion_saga_data = ProfileDeletionSagaData(
        document_type_id=document_type_id,
        tenant_id=tenant_id,
        profile_id=profile_id,
    )

    suts = (
        SagaUnitTestSupport.given()
        .saga(
            ProfileDeletionSaga(steps=profile_deletion_steps),
            profile_deletion_saga_data,
        )
        .expect_completed_successfully()
    )
    saga_data = suts.saga_data

    assert saga_data["tenant_id"] == tenant_id
    assert saga_data["document_type_id"] == document_type_id
    assert saga_data["profile_id"] == profile_id


@pytest.mark.profile_deletion_saga
def test_profile_deletion_saga_failed(
    document_type_id,
    test_tenant_id,
    profile_id,
    profile_deletion_steps,
    fake_document_type_repository: IDocumentTypeRepository,
):
    profile_deletion_saga_data = ProfileDeletionSagaData(
        document_type_id=document_type_id,
        tenant_id=test_tenant_id,
        profile_id=profile_id,
    )
    expected_exception = DocumentTypeNotFound(document_type_id)
    profile_deletion_steps.delete_profile = mock.Mock(side_effect=expected_exception)
    (
        SagaUnitTestSupport.given()
        .saga(
            ProfileDeletionSaga(steps=profile_deletion_steps),
            profile_deletion_saga_data,
        )
        .expect_exception(expected_exception)
    )
