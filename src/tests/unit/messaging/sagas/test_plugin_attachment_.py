from unittest import mock
from uuid import uuid4

import pytest
from deps_message_flow.sagas.testing_support import *

from deps_output_exporting.domain.model import IDocumentTypeRepository
from deps_output_exporting.messaging.sagas import PluginAttachmentSaga
from deps_output_exporting.messaging.sagas_data import PluginAttachmentSagaData


@pytest.mark.plugin_attachment_saga
def test_plugin_attachment_saga(
    profile_name,
    profile_format,
    plugin_attachment_steps,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type,
    profile_schema_data,
):
    fake_document_type_repository.save(document_type=document_type)

    plugin_attachment_saga_data = PluginAttachmentSagaData(
        profile_id=uuid4().hex,
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
        name=profile_name,
        format_=profile_format(),
        schema_data=profile_schema_data,
    )

    suts = (
        SagaUnitTestSupport.given()
        .saga(
            PluginAttachmentSaga(steps=plugin_attachment_steps),
            plugin_attachment_saga_data,
        )
        .expect_completed_successfully()
    )
    saga_data = suts.saga_data

    assert saga_data["tenant_id"] == document_type.tenant_id()
    assert saga_data["document_type_id"] == document_type.id()
    assert saga_data["name"] == profile_name
    assert saga_data["format"] == profile_format()
    assert saga_data["schema_data"] == profile_schema_data


@pytest.mark.plugin_attachment_saga
def test_plugin_attachment_saga__document_type_not_exist__created(
    profile_name,
    profile_format,
    plugin_attachment_steps,
    document_type,
    profile_schema_data,
    fake_document_type_repository: IDocumentTypeRepository,
):
    plugin_attachment_saga_data = PluginAttachmentSagaData(
        profile_id=uuid4().hex,
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
        name=profile_name,
        format_=profile_format(),
        schema_data=profile_schema_data,
    )

    suts = (
        SagaUnitTestSupport.given()
        .saga(
            PluginAttachmentSaga(steps=plugin_attachment_steps),
            plugin_attachment_saga_data,
        )
        .expect_completed_successfully()
    )
    saga_data = suts.saga_data

    assert saga_data["tenant_id"] == document_type.tenant_id()
    assert saga_data["document_type_id"] == document_type.id()
    assert saga_data["name"] == profile_name
    assert saga_data["format"] == profile_format()
    assert saga_data["schema_data"] == profile_schema_data

    assert fake_document_type_repository.document_type_of_id(
        document_type_id=document_type.id(), tenant_id=document_type.tenant_id()
    )


@pytest.mark.plugin_attachment_saga
def test_plugin_attachment_saga_failed(
    profile_name,
    profile_format,
    plugin_attachment_steps,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type,
    profile_id,
    profile_schema_data,
):
    fake_document_type_repository.save(document_type=document_type)

    plugin_attachment_saga_data = PluginAttachmentSagaData(
        profile_id=uuid4().hex,
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
        name=profile_name,
        format_=profile_format(),
        schema_data=profile_schema_data,
    )
    expected_exception = RuntimeError(profile_id)
    plugin_attachment_steps.create_routing_info = mock.Mock(side_effect=expected_exception)

    suts = (
        SagaUnitTestSupport.given()
        .saga(
            PluginAttachmentSaga(steps=plugin_attachment_steps),
            plugin_attachment_saga_data,
        )
        .expect_rolled_back()
    )
