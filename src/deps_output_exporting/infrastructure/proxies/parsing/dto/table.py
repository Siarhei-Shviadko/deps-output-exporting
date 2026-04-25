from dataclasses import asdict, dataclass
from typing import Any, Optional

__all__ = ["DLCell", "Table", "TableReference"]


@dataclass
class DLCell:
    content: str
    column_index: int
    row_index: int
    column_span: int
    row_span: int
    kind: Optional[str] = None


@dataclass
class Table:
    id: str
    column_count: int
    row_count: int
    cells: list[DLCell]

    def to_dict(self) -> dict[str, Any]:
        return {
            "column_count": self.column_count,
            "row_count": self.row_count,
            "cells": [asdict(cell) for cell in self.cells],
        }

    def add_subtable(self, subtable: "Table") -> None:
        for cell in subtable.cells:
            cell.row_index += self.row_count
            self.cells.append(cell)

        self.row_count += subtable.row_count


@dataclass
class TableReference:
    page_number: int
    table_id: str
