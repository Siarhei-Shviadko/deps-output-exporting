from dataclasses import dataclass
from typing import Optional

from ..shared import KeyValueId

__all__ = ["ErrorDetail", "ValidationDetail", "ValidationInfo"]


@dataclass
class ErrorDetail:
    column: Optional[int]
    row: Optional[int]
    index: Optional[int]
    kv_id: Optional[KeyValueId]


@dataclass
class ValidationDetail:
    field_code: str
    errors: list[ErrorDetail]


@dataclass
class ValidationInfo:
    is_valid: bool
    detail: list[ValidationDetail]
