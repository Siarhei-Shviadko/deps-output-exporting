from typing import Any

from deps_output_exporting.domain.model import Code, ExternalStorageInfo

from .one_drive_credentials_mapper import OneDriveCredentialsMapper
from .salesforce_credentials_mapper import SalesforceCredentialsMapper

__all__ = ["ExternalStorageInfoMapper"]


class ExternalStorageInfoMapper:
    @staticmethod
    def from_dict(raw_external_storage_info: dict[str, Any]) -> ExternalStorageInfo:
        code = raw_external_storage_info["code"]

        if code == Code.SALESFORCE:
            credentials = SalesforceCredentialsMapper().from_str(raw_external_storage_info["credentials"])
        elif code == Code.ONE_DRIVE:
            credentials = OneDriveCredentialsMapper().from_str(raw_external_storage_info["credentials"])

        return ExternalStorageInfo(
            code=Code(raw_external_storage_info["code"]),
            credentials=credentials,
            output_directory_path=raw_external_storage_info["output_directory_path"],
        )

    @staticmethod
    def to_dict(external_storage_info: ExternalStorageInfo) -> dict[str, Any]:
        code = external_storage_info.code

        if code == Code.SALESFORCE:
            crypted_credentials = SalesforceCredentialsMapper().to_str(external_storage_info.credentials)
        elif code == Code.ONE_DRIVE:
            crypted_credentials = OneDriveCredentialsMapper().to_str(external_storage_info.credentials)

        return {
            "code": code.value,
            "credentials": crypted_credentials,
            "output_directory_path": external_storage_info.output_directory_path,
        }
