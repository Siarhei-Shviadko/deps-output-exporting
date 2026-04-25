from typing import Optional

from ...shared import FormatCheck, Guard, ImmutableCheck
from .code import Code
from .credentials import Credentials

__all__ = ["ExternalStorageInfo"]

PATH_FORMAT = r"^(?!\/)(?!.*\/$)[\w\/.-]+$"


class ExternalStorageInfo:
    code = Guard[Code](Code, ImmutableCheck())
    credentials = Guard[Credentials](Credentials, ImmutableCheck())
    output_directory_path = Guard[str](str, ImmutableCheck(), FormatCheck(PATH_FORMAT))

    def __init__(self, code: Code, credentials: Credentials, output_directory_path: Optional[str] = None):
        self.code = code
        self.credentials = credentials
        if output_directory_path is not None:
            self.output_directory_path = output_directory_path

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.code == other.code
            and self.credentials == other.credentials
            and self.output_directory_path == other.output_directory_path
        )

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.code = },",
                f"{self.credentials = },",
                f"{self.output_directory_path = }>",
            ),
        )
