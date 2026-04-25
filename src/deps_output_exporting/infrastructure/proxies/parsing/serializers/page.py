from pydantic import Field

from ...base_serializer import ConfiguredBaseModel
from ..dto import DocumentLayout, Page
from .key_value_pair import SerializedKeyValuePair
from .paragraph import SerializedParagraph
from .table import SerializedMergedTable, SerializedTable

__all__ = ["SerializedDocumentLayout"]


class SerializedPage(ConfiguredBaseModel):
    page_number: int
    parsing_type: str
    paragraphs: list[SerializedParagraph]
    tables: list[SerializedTable]
    key_value_pairs: list[SerializedKeyValuePair]

    def to_model(self) -> Page:
        return Page(
            page_number=self.page_number,
            paragraphs=[paragraph.to_model() for paragraph in self.paragraphs],
            tables=[table.to_model() for table in self.tables],
            key_value_pairs=[kvp.to_model() for kvp in self.key_value_pairs],
        )


class SerializedDocumentLayout(ConfiguredBaseModel):
    pages: list[SerializedPage]
    merged_tables: dict[str, list[SerializedMergedTable]] = Field(
        default_factory=dict,
        alias="mergedTables",
    )

    def to_model(self) -> DocumentLayout:
        page_parsing_types = self.pages[0].parsing_type
        merged_tables = [
            [table.to_model() for table in item.tables]
            for parsing_type, elem in self.merged_tables.items()
            if parsing_type == page_parsing_types
            for item in elem  # noqa: WPS361
        ]
        return DocumentLayout(
            pages=[page.to_model() for page in self.pages],
            merged_tables=merged_tables,
        )
