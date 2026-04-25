from datetime import datetime

import pytest

from deps_output_exporting.infrastructure import DLCell, KeyValuePair, Page, Table
from deps_output_exporting.infrastructure.services.document_layout import (
    ExcelBuilder,
    GeneralInfo,
)

FIRST_ELEMENT = 0
SECOND_ELEMENT = 1


@pytest.fixture
def general_info() -> GeneralInfo:
    return GeneralInfo(
        title="Document Title",
        type="AllFieldTypesQA",
        uploaded_date=datetime.fromisoformat("2023-12-11T11:52:02.004368-05:00"),
        pages_number=3,
        engine="TESSERACT",
    )


@pytest.fixture
def excel_builder(general_info, document_layout) -> ExcelBuilder:
    return ExcelBuilder(general_info=general_info, document_layout=document_layout)


@pytest.fixture
def page1(document_layout) -> Page:
    return document_layout.pages[FIRST_ELEMENT]


@pytest.fixture
def page2(document_layout) -> Page:
    return document_layout.pages[SECOND_ELEMENT]


@pytest.fixture
def kvp1(page1) -> KeyValuePair:
    return page1.key_value_pairs[FIRST_ELEMENT]


@pytest.fixture
def kvp2(page1) -> KeyValuePair:
    return page1.key_value_pairs[SECOND_ELEMENT]


@pytest.fixture
def kvp3(page2) -> KeyValuePair:
    return page2.key_value_pairs[FIRST_ELEMENT]


@pytest.fixture
def kvp4(page2) -> KeyValuePair:
    return page2.key_value_pairs[SECOND_ELEMENT]


@pytest.fixture
def table1(page1) -> Table:
    return page1.tables[FIRST_ELEMENT]


@pytest.fixture
def table2(page2) -> Table:
    return page2.tables[FIRST_ELEMENT]


@pytest.fixture
def cell1(table1) -> DLCell:
    return table1.cells[FIRST_ELEMENT]


@pytest.fixture
def cell2(table1) -> DLCell:
    return table1.cells[SECOND_ELEMENT]


@pytest.fixture
def cell3(table2) -> DLCell:
    return table2.cells[FIRST_ELEMENT]


@pytest.fixture
def cell4(table2) -> DLCell:
    return table2.cells[SECOND_ELEMENT]


@pytest.fixture
def excel_builder_with_key_values(general_info, document_layout, key_values) -> ExcelBuilder:
    return ExcelBuilder(general_info=general_info, document_layout=document_layout).with_key_values(key_values)
