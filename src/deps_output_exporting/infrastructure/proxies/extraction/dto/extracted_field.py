from dataclasses import dataclass
from typing import Any, Optional, Union

from ...shared import FieldType, ValidationResult

__all__ = [
    "GenericData",
    "KeyValuePairData",
    "TableData",
    "ExtractedField",
    "Cell",
    "Coordinates",
    "FieldData",
]


@dataclass
class GenericData:
    value: Optional[Union[bool, str]]
    confidence: Optional[float]
    source_id: Optional[str]
    validation_result: ValidationResult = ValidationResult.NOT_APPLIED

    def mark_as_valid(self) -> None:
        self.validation_result = ValidationResult.PASSED

    def to_dict(self) -> Optional[Union[bool, str]]:
        return self.value


@dataclass
class KeyValuePairData:
    key: GenericData
    value: GenericData

    def mark_as_valid(self) -> None:
        self.key.validation_result = ValidationResult.PASSED
        self.value.validation_result = ValidationResult.PASSED

    def to_dict(self) -> dict[str, str]:
        return {self.key.value: self.value.value}  # type: ignore


@dataclass
class Coordinates:
    column_index: int
    row_index: int
    colspan: int
    rowspan: int


@dataclass
class Cell:
    value: str
    confidence: Optional[float]
    coordinates: Coordinates
    source_id: str
    validation_result: ValidationResult = ValidationResult.NOT_APPLIED


@dataclass
class TableData:
    row_count: int
    column_count: int
    cells: list[Cell]
    header_row: Optional[list[str]] = None

    def mark_as_valid(self) -> None:
        for cell in self.cells:
            cell.validation_result = ValidationResult.PASSED

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_count": self.row_count,
            "column_count": self.column_count,
            "cells": [cell.value for cell in self.cells],
            "header_row": self.header_row,
        }


FieldData = Union[
    GenericData,
    KeyValuePairData,
    TableData,
    list[GenericData],
    list[KeyValuePairData],
    list[TableData],
]


@dataclass
class ExtractedField:
    code: str
    data: FieldData
    name: Optional[str] = None
    type: Optional[FieldType] = None
    base_type: Optional[FieldType] = None
    page: Optional[int] = None

    def to_dict(self) -> tuple[str, Any]:
        if isinstance(self.data, list):
            return (self.name, [item.to_dict() for item in self.data])
        return (self.name, self.data.to_dict())
