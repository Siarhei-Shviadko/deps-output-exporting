import pytest
from deps_message_flow.commands.consumer import CommandMessage
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_output_exporting.domain.model import (
    DocumentTypeChanged,
    DocumentTypeCreated,
    DocumentTypeDeleted,
    DocumentTypeFactory,
    GetDocumentTypesReply,
)
from deps_output_exporting.messaging.sagas_data import (
    ProfileCreationSteps,
    ProfileDeletionSteps,
)


@pytest.fixture(name="cmm")
def command_message_mock(mocker):
    return mocker.Mock(CommandMessage)


@pytest.fixture(name="dee")
def domain_event_envelope(mocker):
    return mocker.Mock(DomainEventEnvelope)


@pytest.fixture
def document_type(document_type_id, test_tenant_id):
    return DocumentTypeFactory.create(document_type_id, test_tenant_id)


@pytest.fixture
def get_document_type_reply_message(cmm, test_tenant_id, document_type_id):
    cmm.command = GetDocumentTypesReply(
        document_types=[{"document_type_id": document_type_id, "tenant_id": test_tenant_id}]
    )
    return cmm


@pytest.fixture
def document_type_created_message(dee, test_tenant_id, document_type_id):
    dee.event = DocumentTypeCreated(document_type=document_type_id, tenant=test_tenant_id)
    return dee


@pytest.fixture
def document_type_deleted_message(dee, test_tenant_id, document_type_id):
    dee.event = DocumentTypeDeleted(document_type=document_type_id, tenant=test_tenant_id)
    return dee


@pytest.fixture
def document_type_changed_message(dee, faker):
    dee.event = DocumentTypeChanged(document_id=str(faker.random_int()))
    return dee


@pytest.fixture
def profile_creation_steps(document_type_service, routing_info_service):
    return ProfileCreationSteps(
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
    )


@pytest.fixture
def profile_deletion_steps(document_type_service, routing_info_service):
    return ProfileDeletionSteps(
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
    )
