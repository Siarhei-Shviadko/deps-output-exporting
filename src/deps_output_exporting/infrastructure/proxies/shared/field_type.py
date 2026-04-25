from enum import Enum

__all__ = ["FieldType", "GENERIC_TYPES"]


class FieldType(str, Enum):
    TABLE = "table"
    STRING = "string"
    CHECKMARK = "checkmark"
    LIST = "list"
    DICT = "dict"
    ENUM = "enum"
    DATE = "date"


GENERIC_TYPES = frozenset((FieldType.CHECKMARK, FieldType.DATE, FieldType.ENUM, FieldType.STRING))
