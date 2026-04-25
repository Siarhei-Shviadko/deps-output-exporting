from ..base_serializer import ConfiguredBaseModel
from .unified_data import UnifiedData

__all__ = ["SerializedUnifiedData"]


class SerializedUnifiedDataElement(ConfiguredBaseModel):
    id: str
    page: int


class SerializedUnifiedData(ConfiguredBaseModel):
    elements: list[SerializedUnifiedDataElement]

    def to_model(self) -> list[UnifiedData]:
        return [UnifiedData(id=el.id, page=el.page) for el in self.elements]
