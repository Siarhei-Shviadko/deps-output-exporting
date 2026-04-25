from typing import Optional

from deps_output_exporting.infrastructure.proxies import (
    GENERIC_TYPES,
    Cell,
    DocTypeField,
    ErrorDetail,
    ExtractedField,
    FieldData,
    FieldType,
    GenericData,
    KeyValueId,
    KeyValuePairData,
    TableData,
    UnifiedData,
    ValidationDetail,
    ValidationInfo,
    ValidationResult,
)

from .empty_extracted_fields_factory import EmptyExtractedFieldsFactory

__all__ = ["FieldsMapper"]


class FieldsMapper:
    def __init__(
        self,
        extracted_fields_dict: dict[str, ExtractedField],
        schema_field_codes: list[str],
        is_empty_default_profile: bool,
    ) -> None:
        self._extracted_fields_dict: dict[str, ExtractedField] = extracted_fields_dict
        self._schema_field_codes: list[str] = schema_field_codes
        self._is_empty_default_profile = is_empty_default_profile

    @classmethod
    def for_extracted_fields(
        cls,
        extracted_fields: list[ExtractedField],
        schema_field_codes: list[str],
        is_default_profile: bool,
    ) -> "FieldsMapper":
        is_empty_default_profile = is_default_profile and not schema_field_codes

        if is_empty_default_profile:
            schema_field_codes = [field.code for field in extracted_fields]

        extracted_fields_dict = {
            efield.code: efield for efield in extracted_fields if efield.code in schema_field_codes
        }
        return cls(extracted_fields_dict, schema_field_codes, is_empty_default_profile)

    def add_type_info(self, doc_type_fields: list[DocTypeField]) -> "FieldsMapper":
        doc_type_fields_dict = {dfield.code: dfield for dfield in doc_type_fields}

        for code, dfield in doc_type_fields_dict.items():
            if code not in self._schema_field_codes and not self._is_empty_default_profile:
                continue

            efield = self._extracted_fields_dict.get(code)
            empty_ef_factory = EmptyExtractedFieldsFactory.for_document_type_field(dfield)

            if efield is not None:
                efield.name = dfield.name
                efield.type = dfield.type
                efield.base_type = dfield.base_type
                if dfield.header_row is not None:
                    efield.data = self._add_header_row(efield.data, dfield.header_row)
            elif empty_ef_factory.supports_this_type():
                self._extracted_fields_dict[code] = empty_ef_factory.make_empty_extracted_field()

        return self

    def add_unifier_info(self, unified_data: list[UnifiedData]) -> "FieldsMapper":
        unifier_dict = {data.id: data.page for data in unified_data}
        for field in self._extracted_fields_dict.values():
            if field.type == FieldType.LIST:
                source_id = self._get_source_id(field.base_type, field.data[0])
            else:
                source_id = self._get_source_id(field.type, field.data)
            field.page = unifier_dict.get(source_id)

        return self

    def add_validation_info(self, validation_info: Optional[ValidationInfo]) -> "FieldsMapper":
        if validation_info is not None:
            if validation_info.is_valid is True:
                for field in self._extracted_fields_dict.values():
                    self._mark_field_as_valid(field.data)
            else:
                self._add_validation_errors(validation_info.detail)

        return self

    def get_result(self) -> list[ExtractedField]:
        return list(self._extracted_fields_dict.values())

    def _add_header_row(self, efield_data: FieldData, dfield_header_row: list[str]) -> FieldData:
        if isinstance(efield_data, TableData):
            efield_data.header_row = dfield_header_row
        elif isinstance(efield_data, list):
            for item_data in efield_data:
                self._add_header_row(item_data, dfield_header_row)
        return efield_data

    def _get_source_id(self, field_type: FieldType, field_data: FieldData) -> str:
        if field_type == FieldType.TABLE:
            return field_data.cells[0].source_id
        elif field_type == FieldType.DICT:
            return field_data.key.source_id if field_data.key else field_data.value.source_id
        elif field_type in GENERIC_TYPES:
            return field_data.source_id

    def _add_validation_errors(self, detail: list[ValidationDetail]) -> None:
        validation_errors_dict = {d.field_code: d.errors for d in detail}

        for field_code, field in self._extracted_fields_dict.items():
            if errors := validation_errors_dict.get(field_code):
                if field.type in GENERIC_TYPES:
                    field.data.validation_result = ValidationResult.FAILED
                elif field.type == FieldType.DICT:
                    self._add_dict_errors(errors, field.data)
                elif field.type == FieldType.TABLE:
                    self._add_table_cells_errors(errors, field.data.cells)
                elif field.type == FieldType.LIST:
                    if field.base_type in GENERIC_TYPES:
                        self._add_generic_list_errors(errors, field.data)
                    elif field.base_type == FieldType.DICT:
                        self._add_dict_list_errors(errors, field.data)
                    elif field.base_type == FieldType.TABLE:
                        self._add_table_list_cells_errors(errors, field.data)
            else:
                self._mark_field_as_valid(field.data)

    def _mark_field_as_valid(self, field_data: FieldData) -> None:
        if isinstance(field_data, list):
            for data in field_data:
                data.mark_as_valid()
        else:
            field_data.mark_as_valid()

    def _add_dict_errors(self, errors: list[ErrorDetail], data: KeyValuePairData) -> None:
        dict_errors = [er.kv_id for er in errors]
        data.key.validation_result = (
            ValidationResult.FAILED if KeyValueId.KEY in dict_errors else ValidationResult.PASSED
        )
        data.value.validation_result = (
            ValidationResult.FAILED if KeyValueId.VALUE in dict_errors else ValidationResult.PASSED
        )

    def _add_table_cells_errors(self, errors: list[ErrorDetail], cells: list[Cell]) -> None:
        cells_errors = {(er.column, er.row) for er in errors}
        required_field_error_present = (None, None) in cells_errors
        for cell in cells:
            cell_coords = (cell.coordinates.column_index, cell.coordinates.row_index)
            if cell_coords in cells_errors:
                cell.validation_result = ValidationResult.FAILED
            elif not required_field_error_present:
                cell.validation_result = ValidationResult.PASSED

    def _add_generic_list_errors(self, errors: list[ErrorDetail], data: list[GenericData]) -> None:
        generic_list_errors = [er.index for er in errors]
        for index, item in enumerate(data):
            item.validation_result = (
                ValidationResult.FAILED if index in generic_list_errors else ValidationResult.PASSED
            )

    def _add_dict_list_errors(self, errors: list[ErrorDetail], data: list[KeyValuePairData]) -> None:
        dict_list_errors = [(er.index, er.kv_id) for er in errors]
        for index, item in enumerate(data):
            item.key.validation_result = (
                ValidationResult.FAILED if (index, KeyValueId.KEY) in dict_list_errors else ValidationResult.PASSED
            )
            item.value.validation_result = (
                ValidationResult.FAILED if (index, KeyValueId.VALUE) in dict_list_errors else ValidationResult.PASSED
            )

    def _add_table_list_cells_errors(self, errors: list[ErrorDetail], data: list[TableData]) -> None:
        table_list_errors = {(er.index, er.column, er.row) for er in errors}
        required_field_error_present = (None, None, None) in table_list_errors
        for index, item in enumerate(data):
            for cell in item.cells:
                item_cell_coords = (index, cell.coordinates.column_index, cell.coordinates.row_index)
                if item_cell_coords in table_list_errors:
                    cell.validation_result = ValidationResult.FAILED
                elif not required_field_error_present:
                    cell.validation_result = ValidationResult.PASSED
