from typing import TypedDict, Union

__all__ = ["CredentialsData", "OneDriveCredentialsData", "SalesforceCredentialsData"]


CredentialsData = Union["OneDriveCredentialsData", "SalesforceCredentialsData"]


class OneDriveCredentialsData(TypedDict, total=False):
    client_id: str
    secret: str
    tenant_id: str
    user_id: str


class SalesforceCredentialsData(TypedDict, total=False):
    client_id: str
    client_secret: str
    owner_id: str
    location_id: str
