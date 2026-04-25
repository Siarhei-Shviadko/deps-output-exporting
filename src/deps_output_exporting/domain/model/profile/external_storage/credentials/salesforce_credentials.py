import base64

from ....shared import Guard, ImmutableCheck

__all__ = ["SalesforceCredentials"]


class SalesforceCredentials:
    client_id = Guard[str](str, ImmutableCheck())
    client_secret = Guard[str](str, ImmutableCheck())
    owner_id = Guard[str](str, ImmutableCheck())
    location_id = Guard[str](str, ImmutableCheck())

    def __init__(self, client_id: str, client_secret: str, owner_id: str, location_id: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.owner_id = owner_id
        self.location_id = location_id

    @property
    def basic_token(self) -> str:
        token = ":".join([self.client_id, self.client_secret]).encode("utf-8")
        return base64.b64encode(token).decode("utf-8")

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)  # noqa: WPS222
            and self.client_id == other.client_id
            and self.client_secret == other.client_secret
            and self.owner_id == other.owner_id
            and self.location_id == other.location_id
        )

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.client_id = },",
                f"{self.client_secret = },",
                f"{self.owner_id = },",
                f"{self.location_id = }>",
            ),
        )
