import logging

from deps_message_flow.events.publisher import DomainEventPublisher
from deps_message_flow.sagas.orchestration import Saga, SagaInstanceFactory
from more_itertools import first

from deps_output_exporting.domain.exceptions import DocumentTypeNotFound
from deps_output_exporting.domain.model import (
    DocumentType,
    ExportingType,
    IDocumentTypeRepository,
    IOutputRepository,
    Output,
)
from deps_output_exporting.infrastructure.services import OutputBuildingService
from deps_output_exporting.messaging.sagas import OutputCreationSaga
from deps_output_exporting.messaging.sagas_data import OutputCreationSagaData

__all__ = ["OutputServiceWithSagas"]


class OutputServiceWithSagas:
    def __init__(
        self,
        saga_instance_factory: SagaInstanceFactory,
        sagas: list[Saga],
        document_type_repository: IDocumentTypeRepository,
        output_repository: IOutputRepository,
        output_building_service: OutputBuildingService,
        domain_event_publisher: DomainEventPublisher,
    ):
        self._sagas = {saga.__class__: saga for saga in sagas}
        self._saga_instance_factory = saga_instance_factory
        self._document_type_repository = document_type_repository
        self._output_building_service = output_building_service
        self._output_repository = output_repository
        self._domain_event_publisher = domain_event_publisher

        self._logger = logging.getLogger(self.__class__.__name__)

    def build_output_nosave(self, document_id: str, tenant_id: str, document_type_id: str, profile_id: str) -> Output:
        document_type = self._find_document_type(document_type_id, tenant_id)
        profile = document_type.get_profile(profile_id)

        return self._output_building_service.build(document_id, tenant_id, profile, document_type_id)

    def build_outputs(
        self,
        document_id: str,
        document_type_id: str,
        tenant_id: str,
        profile_ids: list[str] | None,
        routing_info: dict[str, str] | None = None,
    ) -> None:
        if profile_ids is None:
            profile_ids = self._get_plugin_profile_ids(document_type_id=document_type_id, tenant_id=tenant_id)

        if not profile_ids:
            self._logger.warning("No profile ids provided. Skipping.")
            return

        build_outputs_saga_data = OutputCreationSagaData(
            document_type_id=document_type_id,
            document_id=document_id,
            tenant_id=tenant_id,
            profile_id=first(profile_ids),
            routing_info=routing_info,
        )
        si = self._saga_instance_factory.create(self._sagas[OutputCreationSaga], build_outputs_saga_data)
        self._logger.info("Saga %s for profile creation is created", si.saga_id)

    def _get_plugin_profile_ids(self, document_type_id: str, tenant_id: str) -> list[str]:
        document_type = self._find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        return [p.id() for p in document_type.profiles.values() if p.exporting_type == ExportingType.PLUGIN]

    def _find_document_type(self, document_type_id: str, tenant_id: str) -> DocumentType:
        if (document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)) is None:
            raise DocumentTypeNotFound(document_type_id)

        return document_type
