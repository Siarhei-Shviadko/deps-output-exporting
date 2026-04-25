from ..base_serializer import ConfiguredBaseModel
from .kv_data import KeyValue, KeyValues

__all__ = ["SerializedKeyValues", "SerializedKeyValue"]


class SerializedKeyValue(ConfiguredBaseModel):
    key: str
    value: str

    def to_model(self) -> KeyValue:
        return KeyValue(
            key=self.key,
            value=self.value,
        )


class SerializedKeyValues(ConfiguredBaseModel):
    key_values: list[SerializedKeyValue]

    def to_model(self) -> KeyValues:
        return KeyValues(key_values=[kv.to_model() for kv in self.key_values])
