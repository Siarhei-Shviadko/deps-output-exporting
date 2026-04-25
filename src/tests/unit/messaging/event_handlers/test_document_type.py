from deps_output_exporting.domain.model import DocumentTypeFactory
from deps_output_exporting.messaging.handlers import (
    document_type_changed_handler,
    document_type_created_handler,
    document_type_deleted_handler,
)


def test_document_type_created_handler__document_type_created(
    document_type_created_message, fake_document_type_repository, document_type_id, test_tenant_id
):
    document_type_created_handler(document_type_created_message)
    assert fake_document_type_repository.document_type_of_id(document_type_id, test_tenant_id)


def test_document_type_deleted_handler__document_type_deleted(
    document_type_deleted_message, fake_document_type_repository, document_type_id, test_tenant_id
):
    document_type = DocumentTypeFactory.create(document_type_id, test_tenant_id)
    fake_document_type_repository.save(document_type)
    assert fake_document_type_repository.document_type_of_id(document_type_id, test_tenant_id)
    document_type_deleted_handler(document_type_deleted_message)
    assert fake_document_type_repository.document_type_of_id(document_type_id, test_tenant_id) is None


def test_document_type_changed_handler__edata_output_deleted(
    document_type_changed_message, fake_output_repository, output_edata_schema
):
    fake_output_repository.save(output=output_edata_schema)
    document_type_changed_message.event.document_id = output_edata_schema.document_id
    document_type_changed_handler(document_type_changed_message)
    document_outputs = fake_output_repository.find_by_document_id(
        output_edata_schema.tenant_id(), output_edata_schema.document_id
    )

    assert len(document_outputs) == 0


def test_document_type_changed_handler__dl_output_not_deleted(
    document_type_changed_message, fake_output_repository, output_dl_schema
):
    fake_output_repository.save(output=output_dl_schema)
    document_type_changed_message.event.document_id = output_dl_schema.document_id
    document_type_changed_handler(document_type_changed_message)
    document_outputs = fake_output_repository.find_by_document_id(
        output_dl_schema.tenant_id(), output_dl_schema.document_id
    )

    assert len(document_outputs) == 1
