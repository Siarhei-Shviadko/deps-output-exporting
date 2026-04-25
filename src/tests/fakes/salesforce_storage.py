from deps_output_exporting.domain.model import ExternalStorageInfo

__all__ = ["FakeSalesforceStorage"]


class FakeSalesforceStorage:
    def __init__(self) -> None:
        self.storage: dict[str, bytes] = {}

    def upload(self, file_name: str, output_file: bytes, storage_info: ExternalStorageInfo) -> None:
        self.storage[file_name] = output_file
