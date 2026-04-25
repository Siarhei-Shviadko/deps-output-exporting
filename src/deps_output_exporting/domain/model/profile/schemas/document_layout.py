from ...shared import Guard, ImmutableCheck
from .parsing_feature import ParsingFeature
from .parsing_type import ParsingType

__all__ = ["DocumentLayoutSchema"]


class DocumentLayoutSchema:
    parsing_type = Guard[ParsingType](ParsingType, ImmutableCheck())
    features = Guard[list[ParsingFeature]](list, ImmutableCheck())

    def __init__(self, parsing_type: ParsingType, features: list[ParsingFeature]):
        self.parsing_type = parsing_type
        self.features = features

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.parsing_type == self.parsing_type
            and other.features == self.features
        )
