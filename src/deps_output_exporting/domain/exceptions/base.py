__all__ = [
    "OutputExportingException",
    "NotFoundError",
    "IllegalArgument",
    "ForbiddenError",
    "AlreadyExistsError",
    "BusinessException",
]


class OutputExportingException(Exception):
    code = "output_exporting_exception"


class BusinessException(OutputExportingException):
    code = "business_exception"


class NotFoundError(BusinessException):
    code = "not_found_error"


class IllegalArgument(BusinessException):
    code = "illegal_argument"


class ForbiddenError(BusinessException):
    code = "forbidden_error"


class AlreadyExistsError(BusinessException):
    code = "already_exists_error"
