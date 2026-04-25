__all__ = ["FileStorageRequestError", "FileNotFound"]


class FileStorageRequestError(Exception):
    pass


class FileNotFound(Exception):
    pass
