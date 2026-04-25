from dataclasses import asdict

from deps_output_exporting.domain.model import DocumentLayoutSchema, Format, Profile
from deps_output_exporting.infrastructure.proxies import (
    DocumentProxy,
    DocumentTypeProxy,
    ParsingProxy,
    PrompterProxy,
)

from ..output_generator import OutputGenerator
from .excel_builder import ExcelBuilder
from .general_info import GeneralInfo

__all__ = ["DLOutputGenerator"]


class DLOutputGenerator(OutputGenerator):
    def __init__(
        self,
        parsing: ParsingProxy,
        prompter: PrompterProxy,
        document_type: DocumentTypeProxy,
        document: DocumentProxy,
        kvs_output_enabled: bool = False,
    ):
        super().__init__(kvs_output_enabled)

        self._parsing: ParsingProxy = parsing
        self._prompter: PrompterProxy = prompter
        self._document_type = document_type
        self._document = document

    def generate(self, document_id: str, profile: Profile, document_type_id: str) -> bytes:
        if profile.format == Format("json"):
            return self._generate_json_dl_output(document_id, profile.schema)
        elif profile.format == Format("excel"):
            return self._generate_excel_dl_output(document_id, profile.schema, document_type_id)

    def _generate_json_dl_output(self, document_id: str, schema: DocumentLayoutSchema) -> bytes:
        document_layout = self._parsing.get_document_layout(
            document_id=document_id,
            parsing_type=schema.parsing_type,
            features=schema.features,
        ).to_dict(schema.features)

        if self._kvs_output_enabled:
            key_values = self._prompter.get_key_values(document_id)
            document_layout.update(asdict(key_values))

        return self._generate_output_json_file(document_layout)

    def _generate_excel_dl_output(self, document_id: str, schema: DocumentLayoutSchema, document_type_id: str) -> bytes:
        document_layout = self._parsing.get_document_layout(
            document_id=document_id,
            parsing_type=schema.parsing_type,
            features=schema.features,
        )
        document_detail = self._document.get_document_detail(document_id)
        document_type = self._document_type.get_document_type(document_type_id)
        general_info = GeneralInfo.from_document_and_type(
            title=document_detail.title,
            type_=document_type.name,
            uploaded_date=document_detail.date,
            pages_number=len(document_layout.pages),
            engine=document_detail.engine or document_type.engine or self.DEFAULT_ENGINE,
        )

        builder = ExcelBuilder.with_info(general_info=general_info, document_layout=document_layout)

        if self._kvs_output_enabled:
            key_values = self._prompter.get_key_values(document_id).key_values
            builder = builder.with_key_values(key_values)

        return builder.build()
