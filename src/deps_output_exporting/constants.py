import os

PROJECT_NAME = "output-exporting"
DESCRIPTION = "Exports document in specific defined format."
V1_PREFIX = "/v1"
V2_PREFIX = "/v2"
BASE_API_PREFIX = "/api/output-exporting"
V1_API_PREFIX = BASE_API_PREFIX + V1_PREFIX
V2_API_PREFIX = BASE_API_PREFIX + V2_PREFIX
SWAGGER_DOC_URL = "/docs"

DOCUMENTS_EXCHANGER = "Documents"
DOCUMENT_TYPE_EXCHANGER = "DocumentType"

EVENTS_QUEUE = "output-exporting-events"
COMMANDS_QUEUE = "output-exporting-commands"

COMMANDS_CHANNEL = "OutputExportingCommands"
COMMANDS_REPLIES_CHANNEL = "OutputExportingCommandsReplies"

CRYPT_CREDENTIALS_KEY = os.environ.get("CRYPT_CREDENTIALS_KEY", "")

DEFAULT_PROFILE_NAME = "Default Profile"
