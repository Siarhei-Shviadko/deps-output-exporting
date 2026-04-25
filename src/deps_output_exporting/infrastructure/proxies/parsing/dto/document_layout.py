from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

from deps_output_exporting.domain.model import ParsingFeature

from .key_value_pair import KeyValuePair
from .page import Page
from .paragraph import Paragraph
from .table import Table, TableReference

__all__ = ["DocumentLayout"]

TablesByPage = dict[int, dict[str, Table]]


@dataclass
class DocumentLayout:
    pages: list[Page]
    merged_tables: list[list[TableReference]]
    tables: dict[int, list[Table]] = field(init=False)

    def __post_init__(self):
        self.tables = self._construct_tables()

    @cached_property
    def paragraphs(self) -> dict[int, list[Paragraph]]:
        return {page.page_number: page.paragraphs for page in self.pages if page.paragraphs}

    @cached_property
    def key_value_pairs(self) -> dict[int, list[KeyValuePair]]:
        return {page.page_number: page.key_value_pairs for page in self.pages if page.key_value_pairs}

    def to_dict(self, features: list[ParsingFeature]) -> dict[str, Any]:
        return {
            "pages": [
                page.to_dict_with_merged_tables(features, self.tables.get(page.page_number, [])) for page in self.pages
            ],
        }

    def _construct_tables(self) -> dict[int, list[Table]]:
        tables_by_page = self._gather_tables_by_page()

        if self.merged_tables:
            tables_by_page = self._process_merged_tables(tables_by_page)

        return {page_num: list(tables_dict.values()) for page_num, tables_dict in tables_by_page.items()}

    def _gather_tables_by_page(self) -> TablesByPage:
        return {page.page_number: {table.id: table for table in page.tables} for page in self.pages if page.tables}

    def _process_merged_tables(self, tables_by_page: TablesByPage) -> TablesByPage:
        for merged_table in self.merged_tables:
            sorted_subtables = sorted(merged_table, key=lambda item: item.page_number)
            all_subtables = [tables_by_page[ref.page_number].pop(ref.table_id) for ref in sorted_subtables]
            first_subtable = sorted_subtables[0]
            tables_by_page[first_subtable.page_number][first_subtable.table_id] = self._merge_subtables(all_subtables)

        return tables_by_page

    def _merge_subtables(self, subtables: list[Table]) -> Table:
        first_table = subtables[0]
        for table in subtables[1:]:
            first_table.add_subtable(table)
        return first_table
