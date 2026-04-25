import logging

from deps_output_exporting.domain.exceptions import (
    DocumentTypeNotFound,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import (
    IDocumentTypeRepository,
    IRoutingInfoRepository,
    RoutingInfo,
    RoutingInfoFactory,
)

__all__ = ["RoutingInfoService"]


class RoutingInfoService:
    def __init__(
        self,
        document_type_repository: IDocumentTypeRepository,
        routing_info_repository: IRoutingInfoRepository,
    ):
        self._document_type_repository = document_type_repository
        self._routing_info_repository = routing_info_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def create_routing_info(
        self,
        tenant_id: str,
        document_type_id: str,
        profile_id: str,
        command_channel: str,
    ) -> RoutingInfo:
        self._check_document_type_and_profile_existence(
            document_type_id=document_type_id,
            profile_id=profile_id,
            tenant_id=tenant_id,
        )
        routing_info = RoutingInfoFactory.make(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            profile_id=profile_id,
            command_channel=command_channel,
        )
        self._routing_info_repository.save(routing_info)

        return routing_info

    def find_routing_info(self, tenant_id: str, document_type_id: str, profile_id: str) -> RoutingInfo | None:
        return self._routing_info_repository.find(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            profile_id=profile_id,
        )

    def delete_routing_info(
        self,
        tenant_id: str,
        document_type_id: str,
        profile_id: str,
    ) -> None:
        self._routing_info_repository.delete(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            profile_id=profile_id,
        )

    def _check_document_type_and_profile_existence(
        self,
        document_type_id: str,
        profile_id: str,
        tenant_id: str,
    ) -> None:
        document_type = self._document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        if document_type is None:
            raise DocumentTypeNotFound(document_type_id)

        if profile_id not in document_type.profiles:
            raise ProfileNotFound(profile_id)
