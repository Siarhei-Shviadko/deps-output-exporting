from typing import Optional

from ...base_serializer import ConfiguredBaseModel

__all__ = ["SerializedSourceCoordinates"]


class SourceCoordinates(ConfiguredBaseModel):
    source_id: str


class SerializedSourceCoordinates(ConfiguredBaseModel):
    source_bbox_coordinates: Optional[list[SourceCoordinates]]
    source_table_coordinates: Optional[list[SourceCoordinates]]
    source_text_coordinates: Optional[list[SourceCoordinates]]

    def get_source_id(self) -> Optional[str]:
        if self.source_bbox_coordinates is not None:
            return self.source_bbox_coordinates[0].source_id
        elif self.source_table_coordinates is not None:
            return self.source_table_coordinates[0].source_id
        elif self.source_text_coordinates is not None:
            return self.source_text_coordinates[0].source_id
        return None
