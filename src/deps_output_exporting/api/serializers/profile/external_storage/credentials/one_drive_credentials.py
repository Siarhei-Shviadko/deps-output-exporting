from ....base import ConfiguredBaseModel

__all__ = ["SerializedOneDriveCredentials"]


class SerializedOneDriveCredentials(ConfiguredBaseModel):
    client_id: str
    secret: str
    tenant_id: str
    user_id: str
