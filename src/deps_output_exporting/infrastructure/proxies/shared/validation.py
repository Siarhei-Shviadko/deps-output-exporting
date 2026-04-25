from enum import Enum

__all__ = ["ValidationResult", "KeyValueId"]


class ValidationResult(str, Enum):
    PASSED = "Passed"
    FAILED = "Failed"
    NOT_APPLIED = "Not applied"


class KeyValueId(str, Enum):
    KEY = "key"
    VALUE = "value"
