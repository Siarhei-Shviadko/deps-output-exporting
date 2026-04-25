from openpyxl.worksheet.worksheet import Worksheet

from deps_output_exporting.infrastructure.proxies import KeyValue

from .base_filler import BaseFiller

__all__ = ["PrompterKeyValuesFiller"]


class PrompterKeyValuesFiller(BaseFiller):
    KEY_VALUES_VERTICAL_HEADER = ["Key", "Value"]

    def fill_key_values_sheet(self, worksheet: Worksheet, key_values: list[KeyValue]) -> None:
        for kv in key_values:
            self._add_key_or_value(worksheet, self.KEY_VALUES_VERTICAL_HEADER[0], kv.key)
            self._add_key_or_value(worksheet, self.KEY_VALUES_VERTICAL_HEADER[1], kv.value)
            self._add_empty_row(worksheet)

    def _add_key_or_value(self, worksheet: Worksheet, header: str, value: str) -> None:
        worksheet.append([header, value])
        self._add_bold_style_to_odd_cells(worksheet, worksheet.max_row)
