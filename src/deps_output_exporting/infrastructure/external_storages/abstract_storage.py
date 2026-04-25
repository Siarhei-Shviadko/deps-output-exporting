from abc import ABC, abstractmethod

from deps_output_exporting.domain.model import ExternalStorageInfo

__all__ = ["ExternalStorage"]


class ExternalStorage(ABC):
    @abstractmethod
    def upload(self, file_name: str, output_file: bytes, storage_info: ExternalStorageInfo) -> None:
        pass
