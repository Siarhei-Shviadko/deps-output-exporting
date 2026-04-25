from enum import Enum

__all__ = ["OutputState"]


class OutputState(str, Enum):
    PENDING = "pending"
    READY = "ready"
