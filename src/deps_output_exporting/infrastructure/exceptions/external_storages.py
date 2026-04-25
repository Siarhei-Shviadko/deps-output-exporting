from deps_output_exporting.domain.exceptions import OutputExportingException

__all__ = ["OneDriveError", "SalesforceError"]


class OneDriveError(OutputExportingException):
    code = "onedrive_error"


class SalesforceError(OutputExportingException):
    code = "salesforce_error"
