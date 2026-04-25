from typing import Union

from .one_drive_credentials import SerializedOneDriveCredentials
from .salesforce_credentials import SerializedSalesforceCredentials

__all__ = ["SerializedCredentials"]

SerializedCredentials = Union[
    SerializedOneDriveCredentials,
    SerializedSalesforceCredentials,
]
