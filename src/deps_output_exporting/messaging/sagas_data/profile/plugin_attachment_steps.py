import logging
from typing import TYPE_CHECKING

from deps_message_flow.events.publisher import DomainEventPublisher

from deps_output_exporting.domain.model import (
    DocumentTypeFactory,
    IDocumentTypeRepository,
)
from deps_output_exporting.infrastructure import DocumentTypeProxy
from deps_output_exporting.infrastructure.repositories import DocumentTypeRepository

from .plugin_attachment_data import PluginAttachmentSagaData

if TYPE_CHECKING:
    from deps_output_exporting.application import (
        DocumentTypeService,
        RoutingInfoService,
    )

__all__ = ["PluginAttachmentSteps"]


class PluginAttachmentSteps:
    def __init__(
        self,
        document_type_service: "DocumentTypeService",
        routing_info_service: "RoutingInfoService",
        document_type_proxy: "DocumentTypeProxy",
    ) -> None:
        self._document_type_service = document_type_service
        self._routing_info_service = routing_info_service
        self._document_type_proxy: DocumentTypeProxy = document_type_proxy
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_or_create_document_type(self, data: PluginAttachmentSagaData) -> None:  # noqa: WPS463
        document_type_id = self._document_type_proxy.get_or_create_document_type(name=data.name)
        data.document_type_id = document_type_id
        self._logger.info("Created document type: %s", document_type_id)

    def add_profile(self, data: PluginAttachmentSagaData) -> None:
        self._document_type_service.add_plugin_profile(
            profile_id=data.profile_id,
            document_type_id=data.document_type_id,
            tenant_id=data.tenant_id,
            plugin_name=data.name,
            plugin_format=data.format,
            schema_data=data.schema_data,
        )
        self._logger.info("Added profile: %s", data.profile_id)

    def delete_profile(self, data: PluginAttachmentSagaData) -> None:
        self._document_type_service.delete_profile(
            document_type_id=data.entity_id,
            tenant_id=data.tenant_id,
            profile_id=data.profile_id,
        )
        self._logger.info("Deleted profile: %s", data.profile_id)

    def create_routing_info(self, data: PluginAttachmentSagaData) -> None:
        try:
            self._routing_info_service.create_routing_info(
                tenant_id=data.tenant_id,
                document_type_id=data.document_type_id,
                profile_id=data.profile_id,
                command_channel=data.output_plugin_command_channel,
            )
        except Exception as exc:
            self._logger.error(f"RoutingInfo creation error. {str(exc)}", exc_info=True)
            raise RuntimeError(str(exc))
