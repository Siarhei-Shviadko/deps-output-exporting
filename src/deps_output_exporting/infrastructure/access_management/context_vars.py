import contextvars
from typing import Any

__all__ = ["user"]

UserDict = dict[str, Any]
user: contextvars.ContextVar[UserDict] = contextvars.ContextVar("user")
