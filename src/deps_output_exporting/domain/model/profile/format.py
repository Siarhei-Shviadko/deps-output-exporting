__all__ = ["Format"]


class Format:
    def __init__(self, value: str) -> None:
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

    def __eq__(self, other) -> bool:
        return isinstance(other, Format) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
