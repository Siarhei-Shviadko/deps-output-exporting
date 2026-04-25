from typing import Optional

from deps_output_exporting.domain.model import Code, ExternalStorageInfo

from ...base import ConfiguredBaseModel
from .credentials import SerializedCredentials

__all__ = ["SerializedExternalStorageInfo", "GetExternalStorageInfoResponse"]


class SerializedExternalStorageInfo(ConfiguredBaseModel):
    code: Code
    credentials: SerializedCredentials
    output_directory_path: Optional[str] = None


class GetExternalStorageInfoResponse(ConfiguredBaseModel):
    code: Code

    @classmethod
    def from_model(cls, external_storage_info: ExternalStorageInfo) -> "GetExternalStorageInfoResponse":
        return cls(code=external_storage_info.code)
