import pytest

from deps_output_exporting.infrastructure import DocumentTypeProxy
from deps_output_exporting.messaging.sagas_data import (
    OutputCreationSteps,
    PluginAttachmentSteps,
)


@pytest.fixture
def fake_document_type_proxy(external_services, document_type_proxy: DocumentTypeProxy, mocker, document_type_id):
    mock = mocker.Mock(document_type_proxy)
    mock.get_or_create_document_type.return_value = document_type_id
    with external_services.document_type_proxy.override(mock):
        yield external_services.document_type_proxy()


@pytest.fixture()
def plugin_attachment_steps(
    fake_document_type_proxy: DocumentTypeProxy, document_type_service, routing_info_service
) -> PluginAttachmentSteps:
    return PluginAttachmentSteps(
        document_type_proxy=fake_document_type_proxy,
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
    )


@pytest.fixture
def output_creation_steps(
    output_service,
    routing_info_service,
) -> OutputCreationSteps:
    return OutputCreationSteps(output_service=output_service, routing_info_service=routing_info_service)
