import logging

from deps_message_flow.sagas.orchestration_simple_dsl import SimpleSaga

from deps_output_exporting.messaging.sagas_data import (
    ProfileCreationSagaData,
    ProfileCreationSteps,
)

from ..exceptions import SagaFailed, SagaRolledBack

__all__ = ["ProfileCreationSaga"]


class ProfileCreationSaga(SimpleSaga[ProfileCreationSagaData]):
    def __init__(self, steps: ProfileCreationSteps) -> None:
        self._saga_definition = (
            self.step()
            .invoke_local(steps.create_profile)
            .with_compensation(steps.delete_profile)
            .step()
            .invoke_local(steps.create_routing_info)
            .build()
        )

        self._logger = logging.getLogger(self.__class__.__name__)

    def on_saga_completed_successfully(self, saga_id: str, data: ProfileCreationSagaData) -> None:
        self._logger.info(
            "Profile creation saga: `%s` for document type `%s` is completed successfully",
            saga_id,
            data.entity_id,
        )

    def on_saga_rolled_back(self, saga_id: str, data: ProfileCreationSagaData) -> None:
        document_type_id = data.entity_id
        self._logger.warning(
            "Profile creation saga: `%s` for document type `%s` is rolled back",
            saga_id,
            document_type_id,
        )
        raise SagaRolledBack(f"Profile creation saga for document type `{document_type_id}` is rolled back")

    def on_saga_failed(self, saga_id: str, data: ProfileCreationSagaData) -> None:
        document_type_id = data.entity_id
        self._logger.error("Profile creation saga: `%s` for document type `%s` is failed", saga_id, document_type_id)
        raise SagaFailed(f"Profile creation saga for `{document_type_id}` is failed")
