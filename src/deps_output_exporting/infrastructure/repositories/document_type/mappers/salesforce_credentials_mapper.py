import json

from deps_output_exporting.domain.model import SalesforceCredentials

from .abstract_credentials_mapper import AbstractCredentialsMapper

__all__ = ["SalesforceCredentialsMapper"]


class SalesforceCredentialsMapper(AbstractCredentialsMapper):
    def from_str(self, credentials: str) -> SalesforceCredentials:
        decrypted_credentials = json.loads(self._decrypt(credentials))
        return SalesforceCredentials(**decrypted_credentials)

    def to_str(self, credentials: SalesforceCredentials) -> str:
        credentials_to_encrypt = {
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "owner_id": credentials.owner_id,
            "location_id": credentials.location_id,
        }
        return self._encrypt(json.dumps(credentials_to_encrypt))
