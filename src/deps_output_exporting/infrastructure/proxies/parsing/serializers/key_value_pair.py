from typing import Optional

from ...base_serializer import ConfiguredBaseModel
from ..dto import KeyValuePair

__all__ = ["SerializedKeyValuePair"]


class SerializedKeyValuePairElement(ConfiguredBaseModel):
    content: str


class SerializedKeyValuePair(ConfiguredBaseModel):
    key: SerializedKeyValuePairElement
    value: Optional[SerializedKeyValuePairElement] = None
    confidence: Optional[float] = None

    def to_model(self) -> KeyValuePair:
        return KeyValuePair(
            key_content=self.key.content,
            value_content=self.value.content if self.value else None,
            confidence=self.confidence,
        )
