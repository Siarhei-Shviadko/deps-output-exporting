from deps_output_exporting.extras.rest_client import BaseRESTClient, DEPSTokenAuth
from deps_output_exporting.infrastructure.access_management import user

__all__ = ["GenericProxy"]


class GenericProxy(BaseRESTClient):
    def _set_authentication(self) -> None:
        self._session.auth = DEPSTokenAuth(user)
