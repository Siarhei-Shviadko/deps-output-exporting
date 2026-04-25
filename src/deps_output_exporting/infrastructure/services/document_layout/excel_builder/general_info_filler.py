from openpyxl.worksheet.worksheet import Worksheet

from ..general_info import GeneralInfo
from .base_filler import BaseFiller

__all__ = ["GeneralInfoFiller"]


class GeneralInfoFiller(BaseFiller):
    GENERIC_INFO_VERTICAL_HEADER = ["Document Name", "Type", "Uploaded Date", "Number of Pages", "OCR Engine"]

    def add_general_info(self, worksheet: Worksheet, general_info: GeneralInfo) -> None:
        worksheet.append([self.GENERIC_INFO_VERTICAL_HEADER[0], general_info.title])
        worksheet.append([self.GENERIC_INFO_VERTICAL_HEADER[1], general_info.type])
        worksheet.append([self.GENERIC_INFO_VERTICAL_HEADER[2], general_info.uploaded_date.strftime("%d-%m-%Y, %H:%M")])
        worksheet.append([self.GENERIC_INFO_VERTICAL_HEADER[3], general_info.pages_number])
        worksheet.append([self.GENERIC_INFO_VERTICAL_HEADER[4], general_info.engine])
