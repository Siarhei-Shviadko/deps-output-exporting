from typing import Optional

from ..base_serializer import ConfiguredBaseModel
from ..shared import KeyValueId
from .validation_result import ErrorDetail, ValidationDetail, ValidationInfo

__all__ = ["SerializedValidationResult"]


class SerializedValidationError(ConfiguredBaseModel):
    column: Optional[int]
    row: Optional[int]
    index: Optional[int]
    kv_id: Optional[KeyValueId]

    def to_model(self):
        return ErrorDetail(
            column=self.column,
            row=self.row,
            index=self.index,
            kv_id=self.kv_id,
        )


class SerializedValidationDetail(ConfiguredBaseModel):
    field_code: str
    errors: list[SerializedValidationError]

    def to_model(self):
        errors = [SerializedValidationError.to_model(error) for error in self.errors]
        return ValidationDetail(field_code=self.field_code, errors=errors)


class SerializedValidationResult(ConfiguredBaseModel):
    is_valid: bool
    detail: list[SerializedValidationDetail]

    def to_model(self) -> ValidationInfo:
        return ValidationInfo(
            is_valid=self.is_valid,
            detail=[SerializedValidationDetail.to_model(d) for d in self.detail],
        )
