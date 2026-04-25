import json

from deps_output_exporting.domain.model import OneDriveCredentials

from .abstract_credentials_mapper import AbstractCredentialsMapper

__all__ = ["OneDriveCredentialsMapper"]


class OneDriveCredentialsMapper(AbstractCredentialsMapper):
    def from_str(self, credentials: str) -> OneDriveCredentials:
        decrypted_credentials = json.loads(self._decrypt(credentials))
        return OneDriveCredentials(**decrypted_credentials)

    def to_str(self, credentials: OneDriveCredentials) -> str:
        credentials_to_encrypt = {
            "client_id": credentials.client_id,
            "secret": credentials.secret,
            "tenant_id": credentials.tenant_id,
            "user_id": credentials.user_id,
        }
        return self._encrypt(json.dumps(credentials_to_encrypt))
