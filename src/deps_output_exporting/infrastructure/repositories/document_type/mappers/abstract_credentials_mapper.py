from abc import ABC, abstractmethod

from cryptography.fernet import Fernet

from deps_output_exporting.constants import CRYPT_CREDENTIALS_KEY
from deps_output_exporting.domain.model import Credentials


class AbstractCredentialsMapper(ABC):
    def __init__(self):
        self.fernet_key = Fernet(CRYPT_CREDENTIALS_KEY.encode())

    @abstractmethod
    def from_str(self, credentials: str) -> Credentials:
        pass

    @abstractmethod
    def to_str(self, credentials: Credentials) -> str:
        pass

    def _encrypt(self, credentials_to_encrypt: str) -> str:
        return self.fernet_key.encrypt(credentials_to_encrypt.encode()).decode()

    def _decrypt(self, credentials_to_decrypt: str) -> str:
        credentials = credentials_to_decrypt.encode()
        return self.fernet_key.decrypt(credentials.decode())
