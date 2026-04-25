from typing import Optional, TypedDict

from .credentials import CredentialsData

__all__ = ["ExternalStorageInfoData"]


class ExternalStorageInfoData(TypedDict, total=False):
    code: str
    credentials: CredentialsData
    output_directory_path: Optional[str]
