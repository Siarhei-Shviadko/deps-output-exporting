from ..shared import EntityId, TenantId
from .routing_info import RoutingInfo

__all__ = ["RoutingInfoFactory"]


class RoutingInfoFactory:
    @staticmethod
    def make(
        tenant_id: str,
        document_type_id: str,
        profile_id: str,
        command_channel: str,
    ) -> RoutingInfo:
        return RoutingInfo(
            tenant_id=TenantId(tenant_id),
            document_type_id=EntityId(document_type_id),
            profile_id=EntityId(profile_id),
            command_channel=command_channel,
        )
