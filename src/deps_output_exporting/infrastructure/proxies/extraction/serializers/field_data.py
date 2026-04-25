from typing import Optional, Union

from pydantic import StrictBool

from ...base_serializer import ConfiguredBaseModel
from ..dto import Cell, Coordinates, GenericData, KeyValuePairData, TableData
from .base_data import SerializedSourceCoordinates


class SerializedGenericData(SerializedSourceCoordinates):
    value: Optional[Union[StrictBool, str]]
    confidence: Optional[float]

    def to_model(self) -> GenericData:
        return GenericData(value=self.value, confidence=self.confidence, source_id=self.get_source_id())


class SerializedKeyValueFieldData(ConfiguredBaseModel):
    key: SerializedGenericData
    value: SerializedGenericData

    def to_model(self) -> KeyValuePairData:
        return KeyValuePairData(
            key=self.key.to_model(),
            value=self.value.to_model(),
        )


class SerializedCoordinates(ConfiguredBaseModel):
    column: int
    row: int
    colspan: int
    rowspan: int

    def to_model(self) -> Coordinates:
        return Coordinates(
            column_index=self.column,
            row_index=self.row,
            colspan=self.colspan,
            rowspan=self.rowspan,
        )


class SerializedTableCell(SerializedSourceCoordinates):
    value: str
    confidence: Optional[float]
    coordinates: SerializedCoordinates

    def to_model(self) -> Cell:
        return Cell(
            value=self.value,
            confidence=self.confidence,
            coordinates=self.coordinates.to_model(),
            source_id=self.get_source_id(),
        )


class SerializedTableRow(ConfiguredBaseModel):
    y: float


class SerializedTableColumn(ConfiguredBaseModel):
    x: float


class SerializedTableFieldData(ConfiguredBaseModel):
    columns: list[SerializedTableColumn]
    rows: list[SerializedTableRow]
    cells: list[SerializedTableCell]

    def to_model(self) -> TableData:
        return TableData(
            column_count=len(self.columns),
            row_count=len(self.rows),
            cells=[cell.to_model() for cell in self.cells],
        )
