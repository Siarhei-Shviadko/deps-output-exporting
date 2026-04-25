from typing import Optional

from deps_output_exporting.domain.model import ExtractedDataSchema, Format, Profile
from deps_output_exporting.infrastructure.proxies import (
    DocumentProxy,
    DocumentTypeProxy,
    ExtractedField,
    ExtractionProxy,
    HighSparrowProxy,
    UnifierProxy,
    ValidationInfo,
    ValidationProxy,
)

from ..output_generator import OutputGenerator
from .excel_builder import ExcelDataBuilder
from .fields_mapper import FieldsMapper
from .general_info import GeneralInfo

__all__ = ["EdataOutputGenerator"]


class EdataOutputGenerator(OutputGenerator):
    def __init__(
        self,
        extraction: ExtractionProxy,
        document_type: DocumentTypeProxy,
        document: DocumentProxy,
        unifier: UnifierProxy,
        validation: ValidationProxy,
        high_sparrow: HighSparrowProxy,
        new_validation_process: bool,
    ):
        self._extraction: ExtractionProxy = extraction
        self._document_type: DocumentTypeProxy = document_type
        self._document: DocumentProxy = document
        self._unifier: UnifierProxy = unifier
        self._validation: ValidationProxy = validation
        self._high_sparrow: HighSparrowProxy = high_sparrow

        self._output_generators = {
            Format("json"): self._generate_json_edata_output,
            Format("excel"): self._generate_excel_edata_output,
        }

        self._new_validation_process = new_validation_process

    def generate(self, document_id: str, profile: Profile, document_type_id: str) -> bytes:
        return self._output_generators[profile.format](
            document_id=document_id,
            schema=profile.schema,
            document_type_id=document_type_id,
            is_default_profile=profile.is_default(),
        )

    def _generate_json_edata_output(
        self,
        document_id: str,
        schema: ExtractedDataSchema,
        document_type_id: str,
        is_default_profile: bool,
    ) -> bytes:
        edata_fields = self._extraction.get_extracted_data(document_id)
        doc_type_fields = self._document_type.get_document_type(document_type_id).fields

        fields_data = (
            FieldsMapper.for_extracted_fields(edata_fields, schema.fields, is_default_profile)
            .add_type_info(doc_type_fields)
            .get_result()
        )

        return self._generate_output_json_file(dict([field.to_dict() for field in fields_data]))

    def _generate_excel_edata_output(
        self,
        document_id: str,
        schema: ExtractedDataSchema,
        document_type_id: str,
        is_default_profile: bool,
    ) -> bytes:
        document_detail = self._document.get_document_detail(document_id)
        edata_fields = self._extraction.get_extracted_data(document_id)
        doc_type = self._document_type.get_document_type(document_type_id)
        unified_data = self._unifier.get_unified_data(document_id)
        validation_result = self._get_validation_results(schema, document_id)

        fields_data = (
            FieldsMapper.for_extracted_fields(edata_fields, schema.fields, is_default_profile)
            .add_type_info(doc_type.fields)
            .add_unifier_info(unified_data)
            .add_validation_info(validation_result)
            .get_result()
        )

        return ExcelDataBuilder.with_info(
            GeneralInfo.from_document_and_type(
                document_detail.title,
                doc_type.name,
                document_detail.date,
                len(fields_data),
                document_detail.engine or doc_type.engine or self.DEFAULT_ENGINE,
            ),
            fields_data,
        ).build()

    def _get_validation_results(self, schema: ExtractedDataSchema, document_id: str) -> Optional[ValidationInfo]:
        if not schema.needs_validation_results:
            return None

        if self._new_validation_process:
            return self._high_sparrow.get_validation_results(document_id)

        return self._validation.get_validation_results(document_id)
