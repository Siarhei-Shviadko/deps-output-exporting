from typing import Any

from sqlalchemy import Row

from deps_output_exporting.domain.model import EntityId, RoutingInfo, TenantId

__all__ = ["RoutingInfoMapper"]


class RoutingInfoMapper:
    @staticmethod
    def from_row(raw_routing_info: Row) -> RoutingInfo:
        return RoutingInfo(
            tenant_id=TenantId(raw_routing_info.tenant_id),
            document_type_id=EntityId(raw_routing_info.document_type_id),
            profile_id=EntityId(raw_routing_info.profile_id),
            command_channel=raw_routing_info.command_channel,
        )

    @staticmethod
    def to_dict(routing_info: RoutingInfo) -> dict[str, Any]:
        return {
            "tenant_id": routing_info.tenant_id(),
            "document_type_id": routing_info.document_type_id(),
            "profile_id": routing_info.profile_id(),
            "command_channel": routing_info.command_channel,
        }
