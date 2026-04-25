from .builder import ExternalStorageInfoBuilder
from .external_storage import Code, ExternalStorageInfo
from .raw_data import ExternalStorageInfoData

__all__ = ["ExternalStorageInfoFactory"]


class ExternalStorageInfoFactory:
    @classmethod
    def create_external_storages_info(
        cls,
        external_storages_info: list[ExternalStorageInfoData] = None,
    ) -> list[ExternalStorageInfo]:
        built_external_storages_info = []
        for external_storage_info in external_storages_info:
            built_external_storage_info = (
                ExternalStorageInfoBuilder.with_code(Code(external_storage_info["code"]))
                .with_output_directory_path(external_storage_info["output_directory_path"])
                .with_credentials(external_storage_info["credentials"])
                .build()
            )
            built_external_storages_info.append(built_external_storage_info)
        return built_external_storages_info
