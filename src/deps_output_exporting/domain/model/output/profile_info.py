from ..shared import EntityId, Guard, ImmutableCheck
from .schema_type import SchemaType

__all__ = ["ProfileInfo"]


class ProfileInfo:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    version = Guard[str](str, ImmutableCheck())
    schema_type = Guard[SchemaType](SchemaType, ImmutableCheck())

    def __init__(self, id_: EntityId, version: str, schema_type: SchemaType | None) -> None:
        self.id = id_
        self.version = version

        if schema_type:
            self.schema_type = schema_type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id
