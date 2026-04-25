from abc import ABC, abstractmethod
from typing import Optional

from .routing_info import RoutingInfo

__all__ = ["IRoutingInfoRepository"]


class IRoutingInfoRepository(ABC):
    @abstractmethod
    def save(self, routing_info: RoutingInfo) -> None:
        pass

    @abstractmethod
    def find(self, tenant_id: str, document_type_id: str, profile_id: str) -> Optional[RoutingInfo]:
        pass

    @abstractmethod
    def delete(self, tenant_id: str, document_type_id: str, profile_id: str) -> Optional[RoutingInfo]:
        pass
