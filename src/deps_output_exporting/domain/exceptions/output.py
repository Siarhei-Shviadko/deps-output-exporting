from .base import NotFoundError

__all__ = ["OutputNotFound"]


class OutputNotFound(NotFoundError):
    code = "output_not_found_error"
