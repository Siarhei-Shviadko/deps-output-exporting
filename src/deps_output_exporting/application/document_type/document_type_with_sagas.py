import logging
from typing import Optional

from deps_message_flow.sagas.orchestration import Saga, SagaInstanceFactory

from deps_output_exporting.domain.model import (
    EntityId,
    ExternalStorageInfoData,
    Format,
    SchemaData,
)
from deps_output_exporting.messaging.sagas import (
    ProfileCreationSaga,
    ProfileDeletionSaga,
)
from deps_output_exporting.messaging.sagas.plugin_attachment import PluginAttachmentSaga
from deps_output_exporting.messaging.sagas_data import (
    PluginAttachmentSagaData,
    ProfileCreationSagaData,
    ProfileDeletionSagaData,
)

__all__ = ["DocumentTypeServiceWithSagas"]


class DocumentTypeServiceWithSagas:
    def __init__(
        self,
        saga_instance_factory: SagaInstanceFactory,
        sagas: list[Saga],
    ):
        self._sagas = {saga.__class__: saga for saga in sagas}
        self._saga_instance_factory = saga_instance_factory
        self._logger = logging.getLogger(self.__class__.__name__)

    def attach_plugin(
        self,
        id_: str,
        tenant_id: str,
        name: str,
        format_: str,
        schema_data: SchemaData | None,
    ) -> str:
        plugin_attachment_saga_data = PluginAttachmentSagaData(
            profile_id=id_,
            tenant_id=tenant_id,
            name=name,
            format_=format_,
            schema_data=schema_data,
        )
        si = self._saga_instance_factory.create(self._sagas[PluginAttachmentSaga], plugin_attachment_saga_data)
        self._logger.info("Saga %s for plugin attachment is created", si.saga_id)
        return plugin_attachment_saga_data.output_plugin_command_channel

    def create_profile(
        self,
        document_type_id: str,
        tenant_id: str,
        name: str,
        schema: SchemaData,
        format_: Format,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> EntityId:
        profile_creation_saga_data = ProfileCreationSagaData(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
            name=name,
            schema=schema,
            format_=format_,
            external_storages_info=external_storages_info,
        )

        si = self._saga_instance_factory.create(
            self._sagas[ProfileCreationSaga],
            profile_creation_saga_data,
        )

        self._logger.info("Saga %s for profile creation is created", si.saga_id)

        return profile_creation_saga_data.profile_id

    def delete_profile(self, document_type_id: str, tenant_id: str, profile_id: str) -> None:
        profile_deletion_saga_data = ProfileDeletionSagaData(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
            profile_id=profile_id,
        )
        si = self._saga_instance_factory.create(
            self._sagas[ProfileDeletionSaga],
            profile_deletion_saga_data,
        )

        self._logger.info("Saga %s for profile deletion is created", si.saga_id)
