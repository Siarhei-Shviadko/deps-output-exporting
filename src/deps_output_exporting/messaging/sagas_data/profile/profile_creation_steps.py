import logging
from typing import TYPE_CHECKING

from .profile_creation_data import ProfileCreationSagaData

if TYPE_CHECKING:
    from deps_output_exporting.application import (
        DocumentTypeService,
        RoutingInfoService,
    )

__all__ = ["ProfileCreationSteps"]


class ProfileCreationSteps:
    def __init__(
        self,
        document_type_service: "DocumentTypeService",
        routing_info_service: "RoutingInfoService",
    ) -> None:
        self._document_type_service = document_type_service
        self._routing_info_service = routing_info_service
        self._logger = logging.getLogger(self.__class__.__name__)

    def create_profile(self, data: ProfileCreationSagaData) -> None:
        data.profile_id = self._document_type_service.create_profile(
            document_type_id=data.entity_id,
            tenant_id=data.tenant_id,
            name=data.name,
            schema=data.schema,
            format_=data.format,
            external_storages_info=data.external_storages_info,
        )

    def delete_profile(self, data: ProfileCreationSagaData) -> None:
        self._document_type_service.delete_profile(
            document_type_id=data.entity_id,
            tenant_id=data.tenant_id,
            profile_id=data.profile_id(),
        )

    def create_routing_info(self, data: ProfileCreationSagaData) -> None:
        try:
            self._routing_info_service.create_routing_info(
                tenant_id=data.tenant_id,
                document_type_id=data.entity_id,
                profile_id=data.profile_id(),
                command_channel=data.routing_info_command_channel,
            )
        except Exception as exc:
            self._logger.error(f"RoutingInfo creation error. {str(exc)}", exc_info=True)
            raise RuntimeError(str(exc))
