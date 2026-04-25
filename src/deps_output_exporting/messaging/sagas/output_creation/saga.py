import logging

from deps_message_flow.messaging.producer import IMessageProducer
from deps_message_flow.sagas.orchestration_simple_dsl import SimpleSaga

from deps_output_exporting.messaging.commands import (
    BuildOutputReply,
    PerformExportingReply,
)

from ...error_type import ErrorType
from ...sagas_data import OutputCreationSagaData, OutputCreationSteps
from .saga_reply_builder import SagaReplyBuilder

__all__ = ["OutputCreationSaga"]


class OutputCreationSaga(SimpleSaga[OutputCreationSagaData]):
    def __init__(self, steps: OutputCreationSteps, message_producer: IMessageProducer) -> None:
        self._saga_definition = (
            self.step()
            .invoke_local(steps.create_output)
            .with_compensation(steps.delete_output)
            .step()
            .invoke_local(steps.set_routing_info)
            .step()
            .invoke_participant(OutputCreationSagaData.build_output)
            .on_reply(BuildOutputReply, OutputCreationSagaData.save_build_output_result)
            .step()
            .invoke_local(steps.update_output)
            .build()
        )
        self._message_producer = message_producer
        self._logger = logging.getLogger(self.__class__.__name__)

    def on_saga_completed_successfully(self, saga_id: str, data: OutputCreationSagaData) -> None:
        # fmt: off
        if data.routing_info:
            destination, message = (
                SagaReplyBuilder
                .for_routing_info(data.routing_info)
                .with_success(PerformExportingReply())
            )
            self._message_producer.send(destination, message)
        # fmt: on

        self._logger.info("Saga %s for document %s is completed successfully", saga_id, data.document_id)

    def on_saga_failed(self, saga_id: str, data: OutputCreationSagaData) -> None:
        error_message = f"Saga: {saga_id} for document: {data.document_id} is failed"

        # fmt: off
        if data.routing_info:
            destination, message = (
                SagaReplyBuilder
                .for_routing_info(data.routing_info)
                .with_success(
                    PerformExportingReply(
                        error_type=ErrorType.SYSTEM,
                        error_message=error_message,
                    ),
                )
            )
            self._message_producer.send(destination, message)
        # fmt: on

        self._logger.error(error_message)

    def on_saga_rolled_back(self, saga_id: str, data: OutputCreationSagaData) -> None:
        error_message = f"Saga: {saga_id} for document: {data.document_id} is rolled back"

        # fmt: off
        if data.routing_info:
            destination, message = (
                SagaReplyBuilder
                .for_routing_info(data.routing_info)
                .with_success(
                    PerformExportingReply(
                        error_type=ErrorType.SYSTEM,
                        error_message=error_message,
                    ),
                )
            )
            self._message_producer.send(destination, message)
        # fmt: on

        self._logger.error(error_message)
