from typing import TypeVar

from .one_drive_credentials import OneDriveCredentials
from .salesforce_credentials import SalesforceCredentials

__all__ = ["Credentials"]

Credentials = TypeVar("Credentials", OneDriveCredentials, SalesforceCredentials)
