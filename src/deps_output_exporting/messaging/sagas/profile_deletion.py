import logging

from deps_message_flow.sagas.orchestration_simple_dsl import SimpleSaga

from deps_output_exporting.messaging.sagas_data import (
    ProfileDeletionSagaData,
    ProfileDeletionSteps,
)

from ..exceptions import SagaFailed, SagaRolledBack

__all__ = ["ProfileDeletionSaga"]


class ProfileDeletionSaga(SimpleSaga[ProfileDeletionSagaData]):
    def __init__(self, steps: ProfileDeletionSteps) -> None:
        # fmt: off
        self._saga_definition = (
            self.step()
            .invoke_local(steps.delete_profile)
            .step()
            .invoke_local(steps.delete_routing_info)
            .build()
        )
        # fmt: on

        self._logger = logging.getLogger(self.__class__.__name__)

    def on_saga_completed_successfully(self, saga_id: str, data: ProfileDeletionSagaData) -> None:
        self._logger.info(
            "Profile deletion saga: `%s` for document type `%s` is completed successfully",
            saga_id,
            data.entity_id,
        )

    def on_saga_rolled_back(self, saga_id: str, data: ProfileDeletionSagaData) -> None:
        document_type_id = data.entity_id
        self._logger.warning("Profile deletion saga: `%s` for field `%s` is rolled back", saga_id, document_type_id)
        raise SagaRolledBack(f"Profile deletion saga for document type `{document_type_id}` is rolled back")

    def on_saga_failed(self, saga_id: str, data: ProfileDeletionSagaData) -> None:
        document_type_id = data.entity_id
        self._logger.error("Profile deletion saga: `%s` for document type `%s` is failed", saga_id, document_type_id)
        raise SagaFailed(f"Profile deletion saga for `{document_type_id}` is failed")
