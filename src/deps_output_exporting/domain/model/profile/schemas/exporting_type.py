from enum import StrEnum

__all__ = ["ExportingType"]


class ExportingType(StrEnum):
    BUILT_IN = "builtin"
    PLUGIN = "plugin"
