from typing import Any

from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

__all__ = ["BaseFiller"]


class BaseFiller:
    PAGE_HEADER = "Page"
    EMPTY_ROW: list[Any] = []

    def _add_page_header(self, worksheet: Worksheet, page_number: int) -> None:
        worksheet.append([self.PAGE_HEADER, page_number])
        self._add_bold_style_to_odd_cells(worksheet, worksheet.max_row)

    def _add_empty_row(self, worksheet: Worksheet) -> None:
        worksheet.append(self.EMPTY_ROW)

    @staticmethod
    def _add_bold_style_to_row(worksheet: Worksheet, row_number: int) -> None:
        for cell in worksheet[row_number]:
            cell.font = Font(bold=True)

    @staticmethod
    def _add_bold_style_to_odd_cells(worksheet: Worksheet, row_number: int) -> None:
        for cell in worksheet[row_number]:
            if cell.column % 2:
                cell.font = Font(bold=True)
