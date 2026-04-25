from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from deps_output_exporting.infrastructure.proxies import FieldType

__all__ = ["BaseDataFiller"]


class BaseDataFiller:
    TYPES_REPRESENTATION = {
        FieldType.TABLE: "Table",
        FieldType.STRING: "String",
        FieldType.CHECKMARK: "Checkbox",
        FieldType.LIST: "List",
        FieldType.DICT: "Key-Value Pair",
        FieldType.ENUM: "Enum",
        FieldType.DATE: "Date",
    }

    @staticmethod
    def _create_list_common_header(name: str, page: int, item_type: str) -> list:
        return ["Field name", name, "Page", page, "Type", item_type]

    def _add_bold_style_to_row(self, worksheet: Worksheet, row_number: int) -> None:
        for cell in worksheet[row_number]:
            cell.font = Font(bold=True)

    def _add_bold_style_to_odd_cells(self, worksheet: Worksheet, row_number: int) -> None:
        for cell in worksheet[row_number]:
            if cell.column % 2:
                cell.font = Font(bold=True)
