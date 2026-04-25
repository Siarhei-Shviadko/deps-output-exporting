from unittest import mock
from uuid import uuid4

import pytest
from deps_message_flow.sagas.testing_support import *
from more_itertools import first

from deps_output_exporting.constants import COMMANDS_CHANNEL
from deps_output_exporting.domain.model import IDocumentTypeRepository
from deps_output_exporting.messaging.commands import BuildOutput, BuildOutputReply
from deps_output_exporting.messaging.sagas import OutputCreationSaga
from deps_output_exporting.messaging.sagas_data import OutputCreationSagaData


@pytest.mark.output_creation
def test_output_creation_saga(
    output_creation_steps,
    test_tenant_id,
    fake_document_type_repository: IDocumentTypeRepository,
    fake_message_producer,
    document_type,
    document_id,
):
    fake_document_type_repository.save(document_type=document_type)
    default_profile = first(document_type.profiles.values())
    output_id = uuid4().hex
    output_creation_saga_data = OutputCreationSagaData(
        document_type_id=document_type.id(),
        profile_id=default_profile.id(),
        tenant_id=test_tenant_id,
        document_id=document_id,
    )
    suts = (
        SagaUnitTestSupport.given()
        .saga(
            OutputCreationSaga(steps=output_creation_steps, message_producer=fake_message_producer),
            output_creation_saga_data,
        )
        .expect()
        .command(
            BuildOutput(
                document_id=document_id,
                document_type_id=document_type.id(),
                profile_id=default_profile.id(),
                output_id=output_id,
            )
        )
        .to(COMMANDS_CHANNEL)
        .and_given()
        .success_reply(
            BuildOutputReply(
                document_id=document_id, output_id=output_id, blob_name="a.pdf", error_type=None, error_message=None
            )
        )
        .expect_completed_successfully()
    )
    saga_data = suts.saga_data

    assert saga_data["tenant_id"] == document_type.tenant_id()
    assert saga_data["document_type_id"] == document_type.id()
    assert saga_data["command_channel"] == COMMANDS_CHANNEL
    assert saga_data["output_id"]
    assert saga_data["file_path"] == "a.pdf"


@pytest.mark.output_creation
def test_output_creation_saga_failed(
    output_creation_steps,
    test_tenant_id,
    fake_document_type_repository: IDocumentTypeRepository,
    fake_message_producer,
    document_type,
    document_id,
):
    fake_document_type_repository.save(document_type=document_type)
    default_profile = first(document_type.profiles.values())
    output_id = uuid4().hex
    output_creation_saga_data = OutputCreationSagaData(
        document_type_id=document_type.id(),
        profile_id=default_profile.id(),
        tenant_id=test_tenant_id,
        document_id=document_id,
    )
    expected_exception = RuntimeError(output_id)
    output_creation_steps.set_routing_info = mock.Mock(side_effect=expected_exception)

    (
        SagaUnitTestSupport.given()
        .saga(
            OutputCreationSaga(steps=output_creation_steps, message_producer=fake_message_producer),
            output_creation_saga_data,
        )
        .expect_rolled_back()
    )
