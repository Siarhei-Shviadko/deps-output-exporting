from dataclasses import dataclass
from typing import Any

from deps_output_exporting.domain.model import ParsingFeature

from .key_value_pair import KeyValuePair
from .paragraph import Paragraph
from .table import Table

__all__ = ["Page"]


@dataclass
class Page:
    page_number: int
    paragraphs: list[Paragraph]
    tables: list[Table]
    key_value_pairs: list[KeyValuePair]

    @property
    def feature_mapping(self) -> dict[ParsingFeature, str]:
        return {
            ParsingFeature.TEXT: "paragraphs",
            ParsingFeature.TABLES: "tables",
            ParsingFeature.KEY_VALUE_PAIRS: "key_value_pairs",
        }

    def to_dict(self, features: list[ParsingFeature]) -> dict[str, Any]:
        page_dict: dict[str, Any] = {"page_number": self.page_number}
        for feat in features:
            page_dict[self.feature_mapping[feat]] = [
                item.to_dict() for item in getattr(self, self.feature_mapping[feat])
            ]

        return page_dict

    def to_dict_with_merged_tables(
        self,
        features: list[ParsingFeature],
        full_tables: list[Table],
    ) -> dict[str, Any]:
        page_dict: dict[str, Any] = {"page_number": self.page_number}
        for feat in features:
            if feat is ParsingFeature.TABLES:
                page_dict[self.feature_mapping[feat]] = [table.to_dict() for table in full_tables]
            else:
                page_dict[self.feature_mapping[feat]] = [
                    item.to_dict() for item in getattr(self, self.feature_mapping[feat])
                ]

        return page_dict
