from deps_message_flow.commands.common import CommandReplyOutcome

from deps_output_exporting.messaging.handlers import get_document_types_reply_handler


def test_get_document_types_reply_handler__command_succeed__document_types_created(
    get_document_type_reply_message, fake_document_type_repository, document_type_id, test_tenant_id
):
    get_document_type_reply_message.message.get_required_header.return_value = CommandReplyOutcome.SUCCESS.name
    get_document_types_reply_handler(get_document_type_reply_message)
    assert fake_document_type_repository.document_type_of_id(document_type_id, test_tenant_id)


def test_get_document_types_reply_handler__command_failed__document_types_not_created(
    get_document_type_reply_message, fake_document_type_repository, document_type_id, test_tenant_id
):
    get_document_type_reply_message.message.get_required_header.return_value = CommandReplyOutcome.FAILURE.name
    get_document_types_reply_handler(get_document_type_reply_message)
    assert fake_document_type_repository.document_type_of_id(document_type_id, test_tenant_id) is None
