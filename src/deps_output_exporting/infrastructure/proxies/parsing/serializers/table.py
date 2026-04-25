from typing import Optional

from pydantic import Field

from ...base_serializer import ConfiguredBaseModel
from ..dto import DLCell, Table, TableReference

__all__ = ["SerializedTable"]


class SerializedCell(ConfiguredBaseModel):
    content: str
    kind: Optional[str] = None
    column_index: int
    row_index: int
    column_span: int
    row_span: int

    def to_model(self) -> DLCell:
        return DLCell(
            content=self.content,
            kind=self.kind if self.kind else None,
            column_index=self.column_index,
            row_index=self.row_index,
            column_span=self.column_span,
            row_span=self.row_span,
        )


class SerializedTable(ConfiguredBaseModel):
    id: str
    column_count: int
    row_count: int
    cells: list[SerializedCell]

    def to_model(self) -> Table:
        return Table(
            id=self.id,
            column_count=self.column_count,
            row_count=self.row_count,
            cells=[cell.to_model() for cell in self.cells],
        )


class SerializedTableReference(ConfiguredBaseModel):
    page_number: int = Field(..., alias="pageNumber")
    table_id: str = Field(..., alias="tableId")

    def to_model(self) -> TableReference:
        return TableReference(page_number=self.page_number, table_id=self.table_id)


class SerializedMergedTable(ConfiguredBaseModel):
    parsing_type: str
    tables: list[SerializedTableReference]
