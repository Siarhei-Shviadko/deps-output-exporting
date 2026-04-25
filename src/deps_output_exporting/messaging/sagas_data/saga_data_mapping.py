from deps_message_flow.sagas.orchestration import SagaDataMapping

from .output import OutputCreationSagaData
from .profile import (
    PluginAttachmentSagaData,
    ProfileCreationSagaData,
    ProfileDeletionSagaData,
)

__all__ = ["make_saga_data_mapping"]


def make_saga_data_mapping() -> SagaDataMapping:
    return SagaDataMapping(
        {
            ProfileCreationSagaData.__name__: ProfileCreationSagaData,
            ProfileDeletionSagaData.__name__: ProfileDeletionSagaData,
            PluginAttachmentSagaData.__name__: PluginAttachmentSagaData,
            OutputCreationSagaData.__name__: OutputCreationSagaData,
        },
    )
