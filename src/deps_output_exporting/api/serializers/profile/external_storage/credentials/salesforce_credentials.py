from ....base import ConfiguredBaseModel

__all__ = ["SerializedSalesforceCredentials"]


class SerializedSalesforceCredentials(ConfiguredBaseModel):
    client_id: str
    client_secret: str
    owner_id: str
    location_id: str
