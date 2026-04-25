import logging
from typing import TYPE_CHECKING

from deps_output_exporting.constants import COMMANDS_CHANNEL

if TYPE_CHECKING:
    from deps_output_exporting.application import RoutingInfoService, OutputService
from .output_building_data import OutputCreationSagaData

__all__ = ["OutputCreationSteps"]


class OutputCreationSteps:
    def __init__(self, output_service: "OutputService", routing_info_service: "RoutingInfoService") -> None:
        self._output_service = output_service
        self._routing_info_service = routing_info_service

        self._logger = logging.getLogger(self.__class__.__name__)

    def create_output(self, data: OutputCreationSagaData) -> None:
        output = self._output_service.create_empty_output(
            document_id=data.document_id,
            tenant_id=data.tenant_id,
            document_type_id=data.document_type_id,
            profile_id=data.profile_id,
        )
        data.output_id = output.id()

    def delete_output(self, data: OutputCreationSagaData) -> None:
        self._output_service.delete_output(
            document_id=data.document_id,
            tenant_id=data.tenant_id,
            output_id=data.output_id,
        )

    def set_routing_info(self, data: OutputCreationSagaData) -> None:
        routing_info = self._routing_info_service.find_routing_info(
            tenant_id=data.tenant_id,
            document_type_id=data.document_type_id,
            profile_id=data.profile_id,
        )
        command_channel = (routing_info and routing_info.command_channel) or COMMANDS_CHANNEL
        data.command_channel = command_channel

    def update_output(self, data: OutputCreationSagaData) -> None:
        self._output_service.update_output(
            output_id=data.output_id,
            tenant_id=data.tenant_id,
            document_id=data.document_id,
            new_file_path=data.file_path,
            profile_id=data.profile_id,
        )
