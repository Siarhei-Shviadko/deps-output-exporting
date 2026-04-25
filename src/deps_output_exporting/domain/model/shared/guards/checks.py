import re
from typing import Any, Protocol, Type, TypeVar, get_args

from deps_output_exporting.domain.exceptions import IllegalArgument

from .attribute_name import AttributeName

T = TypeVar("T", contravariant=True)
MAX_LENGTH = 150


__all__ = ["Check", "NoneCheck", "TypeCheck", "ImmutableCheck", "LengthCheck", "FormatCheck"]


class Check(Protocol[T]):
    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        ...  # noqa: WPS428


class NoneCheck:
    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        if value is None:
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} object should be provided.",
            )


class TypeCheck:
    def __init__(self, type_: Any) -> None:
        if hasattr(type_, "__constraints__"):
            self._types = type_.__constraints__
            self._type_name = type_.__name__
        elif "typing" not in str(type_):
            self._types = (type_,)
            self._type_name = type_.__name__
        else:
            self._types = get_args(type_)
            self._type_name = str(type_)

    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        if not isinstance(value, self._types):
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} "
                + f"object should be {self._type_name}.",
            )


class ImmutableCheck:
    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        if hasattr(domain_obj, attribute_name.private) and getattr(domain_obj, attribute_name.private) is not None:
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} object cannot be changed.",
            )


class LengthCheck:
    def is_correct(self, domain_obj: Any, value: str, attribute_name: AttributeName) -> None:
        if len(value) > MAX_LENGTH:
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} object cannot be more "
                f"than {MAX_LENGTH} symblos.",  # noqa: WPS326
            )


class FormatCheck:
    def __init__(self, pattern: str) -> None:
        self._pattern = pattern

    def is_correct(self, domain_obj: Any, value: str, attribute_name: AttributeName) -> None:
        if not re.fullmatch(self._pattern, value):
            raise IllegalArgument(
                (
                    "Attribute {0} for {1} object should not contain special symbols.".format(
                        attribute_name.public,
                        domain_obj.__class__.__name__,
                    )
                ),
            )
