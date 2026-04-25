from datetime import datetime

from deps_output_exporting.domain.model import Output, ProfileInfo

from .base import ConfiguredBaseModel

__all__ = ["BuildOutputRequest", "SerializedOutput", "OutputsListResponse"]


class ProfileInfoResponse(ConfiguredBaseModel):
    id: str
    version: str

    @classmethod
    def from_model(cls, profile_info: ProfileInfo) -> "ProfileInfoResponse":
        return cls(
            id=profile_info.id(),
            version=profile_info.version,
        )


class BuildOutputRequest(ConfiguredBaseModel):
    document_type_id: str
    profile_id: str


class SerializedOutput(ConfiguredBaseModel):
    id: str
    tenant_id: str
    profile_info: ProfileInfoResponse
    document_id: str
    state: str
    file_path: str | None
    creation_date: datetime

    @classmethod
    def from_model(cls, output: Output) -> "SerializedOutput":
        return cls(
            id=output.id(),
            tenant_id=output.tenant_id(),
            profile_info=ProfileInfoResponse.from_model(output.profile_info),
            document_id=output.document_id,
            state=output.state.value,
            file_path=output.file_path,
            creation_date=output.creation_date,
        )


class OutputsListResponse(ConfiguredBaseModel):
    outputs: list[SerializedOutput]
