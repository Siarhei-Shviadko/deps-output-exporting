__all__ = ["FakeFileStorageProxy"]


class FakeFileStorageProxy:
    def __init__(self) -> None:
        self.storage: dict[str, bytes] = {}

    def upload_file(self, file_path: str, file_name: str, output_file: bytes) -> str:
        full_file_path = file_path + file_name
        self.storage[full_file_path] = output_file

        return full_file_path
