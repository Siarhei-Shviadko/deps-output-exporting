__all__ = ["ExtractedDataSchema"]

from ...shared import Guard, ImmutableCheck


class ExtractedDataSchema:
    fields = Guard[list[str]](list, ImmutableCheck())
    needs_validation_results = Guard[bool](bool, ImmutableCheck())

    def __init__(self, fields: list[str], needs_validation_results: bool):
        self.fields = fields
        self.needs_validation_results = needs_validation_results

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.fields == self.fields
            and other.needs_validation_results == self.needs_validation_results
        )
