import json
from abc import ABC, abstractmethod
from typing import Any

from deps_output_exporting.domain.model import Profile

__all__ = ["OutputGenerator"]


class OutputGenerator(ABC):
    DEFAULT_ENGINE = "TESSERACT"

    def __init__(self, kvs_output_enabled: bool = False):
        self._kvs_output_enabled = kvs_output_enabled

    @abstractmethod
    def generate(self, document_id: str, profile: Profile, document_type_id: str) -> bytes:
        pass

    def _generate_output_json_file(self, output_dict: dict[str, Any]) -> bytes:
        output_json = json.dumps(output_dict)
        return output_json.encode("utf8")
