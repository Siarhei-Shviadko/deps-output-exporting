from dataclasses import dataclass

__all__ = ["KeyValue", "KeyValues"]


@dataclass
class KeyValue:
    key: str
    value: str


@dataclass
class KeyValues:
    key_values: list[KeyValue]
