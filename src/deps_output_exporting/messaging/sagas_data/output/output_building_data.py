from types import EllipsisType

from deps_message_flow.commands.consumer import CommandWithDestinationBuilder
from deps_message_flow.sagas.orchestration import SagaData

from deps_output_exporting.messaging.commands import BuildOutput, BuildOutputReply

__all__ = ["OutputCreationSagaData"]


class OutputCreationSagaData(SagaData):
    def __init__(
        self,
        document_type_id: str,
        tenant_id: str,
        document_id: str,
        profile_id: str,
        *,
        output_id: str | None = None,
        command_channel: str | None = None,
        file_path: str | None | EllipsisType = ...,
        routing_info: dict[str, str] | None = None,
    ) -> None:
        super().__init__(entity_id=document_id)

        self.document_type_id = document_type_id
        self.tenant_id = tenant_id
        self.document_id = document_id
        self.profile_id = profile_id
        self.routing_info = routing_info

        self._output_id: str | None = output_id
        self._command_channel: str | None = command_channel
        self._file_path: str | None = file_path  # type: ignore

    @property
    def output_id(self) -> str:
        if not self._output_id:
            raise RuntimeError("Attempting to obtain the output id before it was created")
        return self._output_id

    @output_id.setter
    def output_id(self, output_id: str) -> None:
        self._output_id = output_id

    @property
    def command_channel(self) -> str:
        if not self._command_channel:
            raise RuntimeError("Attempting to obtain the command channel before it was set")
        return self._command_channel

    @command_channel.setter
    def command_channel(self, command_channel: str) -> None:
        self._command_channel = command_channel

    @property
    def file_path(self) -> str | None:
        if self._file_path is ...:
            raise RuntimeError("Attempting to obtain the file path before it was set")
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str | None) -> None:
        self._file_path = file_path

    def build_output(self):
        return (
            CommandWithDestinationBuilder.send(
                BuildOutput(
                    document_id=self.document_id,
                    document_type_id=self.document_type_id,
                    profile_id=self.profile_id,
                    output_id=self.output_id,
                ),
            )
            .to(self.command_channel)
            .build()
        )

    def save_build_output_result(self, reply: BuildOutputReply) -> None:
        if reply.error_type:
            raise RuntimeError(reply.error_message)
        self.file_path = reply.blob_name

    def to_dict(self) -> dict:
        file_path_value = "..." if (self._file_path is ...) else self._file_path
        return {
            "document_id": self.document_id,
            "document_type_id": self.document_type_id,
            "tenant_id": self.tenant_id,
            "profile_id": self.profile_id,
            "output_id": self._output_id,
            "command_channel": self._command_channel,
            "file_path": file_path_value,
            "routing_info": self.routing_info,
        }

    @classmethod
    def from_dict(cls, raw_data: dict) -> "SagaData":
        saved_path_value = raw_data["file_path"]
        file_path_value = ... if (saved_path_value == "...") else saved_path_value
        return cls(
            document_id=raw_data["document_id"],
            document_type_id=raw_data["document_type_id"],
            tenant_id=raw_data["tenant_id"],
            profile_id=raw_data["profile_id"],
            output_id=raw_data["output_id"],
            command_channel=raw_data["command_channel"],
            file_path=file_path_value,
            routing_info=raw_data["routing_info"],
        )
