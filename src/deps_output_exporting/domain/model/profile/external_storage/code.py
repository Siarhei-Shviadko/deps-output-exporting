from enum import Enum

__all__ = ["Code"]


class Code(str, Enum):
    SALESFORCE = "Salesforce"
    ONE_DRIVE = "One Drive"
