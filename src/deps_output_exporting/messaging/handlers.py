import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.common import (
    CommandReplyOutcome,
    ReplyMessageHeaders,
    make_message_for_command,
)
from deps_message_flow.commands.consumer import CommandHandlerReplyBuilder
from deps_message_flow.commands.consumer.command_message import CommandMessage
from deps_message_flow.events.mappers import JsonMapper
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)
from deps_message_flow.messaging.common import IMessage

from deps_output_exporting.api.auth import get_current_user_tenant
from deps_output_exporting.application import (
    DocumentTypeService,
    OutputService,
    OutputServiceWithSagas,
)
from deps_output_exporting.containers import Containers
from deps_output_exporting.domain.exceptions import BusinessException
from deps_output_exporting.domain.model import DocumentTypeData

from .commands import BuildOutput, BuildOutputReply, PerformExporting
from .error_type import ErrorType

logger = logging.getLogger(__name__)

__all__ = [
    "get_document_types_reply_handler",
    "document_type_deleted_handler",
    "document_type_created_handler",
    "document_type_changed_handler",
    "build_output_handler",
    "perform_output_exporting_handler",
]


@inject
def get_document_types_reply_handler(  # noqa: WPS463 - Found a getter without a return value
    command_message: CommandMessage,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
) -> None:
    if is_command_successful(command_message):
        document_types_raw = command_message.command.document_types
        document_types_data: list[DocumentTypeData] = [
            DocumentTypeData(document_type_id=dtr["document_type_id"], tenant_id=dtr["tenant_id"])
            for dtr in document_types_raw
        ]
        document_type_service.save_document_types(document_types_data)
        logger.info("Document types updated successfully")
    else:
        logger.error(f"Failed to get document types. Command headers: {command_message.message.headers}")


@inject
def document_type_created_handler(
    dee: DomainEventEnvelope,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
) -> None:
    document_type_service.save_document_type(document_type_id=dee.event.document_type, tenant_id=dee.event.tenant)


@inject
def document_type_deleted_handler(
    dee: DomainEventEnvelope,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
) -> None:
    document_type_service.delete_document_type(document_type_id=dee.event.document_type, tenant_id=dee.event.tenant)


def is_command_successful(command_message):
    return (
        command_message.message.get_required_header(ReplyMessageHeaders.REPLY_OUTCOME)
        == CommandReplyOutcome.SUCCESS.name
    )


@inject
def document_type_changed_handler(
    dee: DomainEventEnvelope,
    output_service: OutputService = Provide[Containers.output_service],
) -> None:
    output_service.delete_document_edata_outputs(
        document_id=dee.event.document_id,
        tenant_id=get_current_user_tenant(),
    )


@inject
def build_output_handler(
    command_message: CommandMessage[BuildOutput],
    output_service: OutputServiceWithSagas = Provide[Containers.output_service_with_sagas],
    tenant_id: str = Provide[Containers.current_user_tenant],
) -> list[IMessage]:
    error_type = None
    error_message = None
    blob_name = None
    command = command_message.command
    try:
        output = output_service.build_output_nosave(
            document_id=command.document_id,
            tenant_id=tenant_id,
            document_type_id=command.document_type_id,
            profile_id=command.profile_id,
        )
        blob_name = output.file_path

    except BusinessException as e:
        error_type, error_message = ErrorType.BUSINESS, repr(e)
    except Exception as e:
        error_type, error_message = ErrorType.SYSTEM, repr(e)
    if error_type is not None:
        logger.error(f"Failed to export document with id {command.document_id}!\nReason: {error_message}")
    reply = BuildOutputReply(
        document_id=command_message.command.document_id,
        blob_name=blob_name,
        error_type=error_type,
        error_message=error_message,
        output_id=command_message.command.output_id,
    )

    reply_command_message = make_message_for_command(
        channel="NONE",
        payload=JsonMapper().serialize(reply),
        command_type=reply.__class__.__name__,
        reply_to="NONE",
    )

    return [CommandHandlerReplyBuilder.with_success(reply_command_message)]


@inject
def perform_output_exporting_handler(
    command_message: CommandMessage[PerformExporting],
    output_service: OutputServiceWithSagas = Provide[Containers.output_service_with_sagas],
) -> None:
    command = command_message.command

    output_service.build_outputs(
        tenant_id=get_current_user_tenant(),
        document_id=command.document_id,
        document_type_id=command.document_type_id,
        profile_ids=command.profile_ids,
        routing_info=command_message.correlation_headers,
    )
