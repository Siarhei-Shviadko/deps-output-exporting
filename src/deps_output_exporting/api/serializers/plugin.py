from .base import ConfiguredBaseModel
from .schemas import SerializedDocumentLayoutSchema, SerializedExtractedDataSchema

__all__ = ["AttachPluginRequest", "AttachPluginResponse"]


class AttachPluginRequest(ConfiguredBaseModel):
    id: str
    name: str
    format: str
    schema: SerializedDocumentLayoutSchema | SerializedExtractedDataSchema | None


class AttachPluginResponse(ConfiguredBaseModel):
    command_channel: str
