from ....shared import Guard, ImmutableCheck

__all__ = ["OneDriveCredentials"]


class OneDriveCredentials:
    client_id = Guard[str](str, ImmutableCheck())
    secret = Guard[str](str, ImmutableCheck())
    tenant_id = Guard[str](str, ImmutableCheck())
    user_id = Guard[str](str, ImmutableCheck())

    def __init__(self, client_id: str, secret: str, tenant_id: str, user_id: str):
        self.client_id = client_id
        self.secret = secret
        self.tenant_id = tenant_id
        self.user_id = user_id

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)  # noqa: WPS222
            and self.tenant_id == other.tenant_id
            and self.client_id == other.client_id
            and self.secret == other.secret
            and self.user_id == other.user_id
        )

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.client_id = },",
                f"{self.secret = },",
                f"{self.tenant_id = },",
                f"{self.user_id = }>",
            ),
        )
