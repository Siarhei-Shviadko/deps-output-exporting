from .base import NotFoundError

__all__ = ["RoutingInfoNotFound"]


class RoutingInfoNotFound(NotFoundError):
    code = "routing_info_not_found_error"
