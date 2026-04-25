from openpyxl.worksheet.worksheet import Worksheet

from deps_output_exporting.infrastructure.proxies import KeyValuePair

from .base_filler import BaseFiller

__all__ = ["KeyValuePairsFiller"]


class KeyValuePairsFiller(BaseFiller):
    KEY_VALUE_PAIR_HEADER = ["Key", "Value", "PairConfidence"]

    def add_key_value_pairs(
        self,
        worksheet: Worksheet,
        page_numbers_key_value_pairs: dict[int, list[KeyValuePair]],
    ) -> None:
        for page_number, key_value_pairs in page_numbers_key_value_pairs.items():
            self._add_page_header(worksheet=worksheet, page_number=page_number)
            self._add_key_value_pair_header(worksheet)

            for key_value_pair in key_value_pairs:
                worksheet.append([key_value_pair.key_content, key_value_pair.value_content, key_value_pair.confidence])

            self._add_empty_row(worksheet)

    def _add_key_value_pair_header(self, worksheet: Worksheet) -> None:
        worksheet.append(self.KEY_VALUE_PAIR_HEADER)
        self._add_bold_style_to_row(worksheet, worksheet.max_row)
