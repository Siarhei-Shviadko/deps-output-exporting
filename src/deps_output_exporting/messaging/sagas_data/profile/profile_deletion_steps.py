import logging
from typing import TYPE_CHECKING

from .profile_deletion_data import ProfileDeletionSagaData

if TYPE_CHECKING:
    from deps_output_exporting.application import (
        DocumentTypeService,
        RoutingInfoService,
    )

__all__ = ["ProfileDeletionSteps"]


class ProfileDeletionSteps:
    def __init__(
        self,
        document_type_service: "DocumentTypeService",
        routing_info_service: "RoutingInfoService",
    ) -> None:
        self._document_type_service = document_type_service
        self._routing_info_service = routing_info_service
        self._logger = logging.getLogger(self.__class__.__name__)

    def delete_profile(self, data: ProfileDeletionSagaData) -> None:
        self._document_type_service.delete_profile(
            document_type_id=data.entity_id,
            tenant_id=data.tenant_id,
            profile_id=data.profile_id,
        )

    def delete_routing_info(self, data: ProfileDeletionSagaData) -> None:
        self._routing_info_service.delete_routing_info(
            tenant_id=data.tenant_id,
            document_type_id=data.entity_id,
            profile_id=data.profile_id,
        )
