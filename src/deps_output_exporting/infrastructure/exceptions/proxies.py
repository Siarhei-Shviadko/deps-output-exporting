from deps_output_exporting.domain.exceptions import OutputExportingException

__all__ = [
    "ExtractedDataError",
    "DocumentTypeError",
    "DocumentError",
    "UnifierError",
    "ValidationError",
    "ParsingError",
    "PrompterError",
]


class ExtractedDataError(OutputExportingException):
    code = "extracted_data_error"


class DocumentTypeError(OutputExportingException):
    code = "document_type_error"


class DocumentError(OutputExportingException):
    code = "document_error"


class UnifierError(OutputExportingException):
    code = "unifier_error"


class ValidationError(OutputExportingException):
    code = "validation_error"


class ParsingError(OutputExportingException):
    code = "parsing_error"


class PrompterError(OutputExportingException):
    code = "prompter_error"
