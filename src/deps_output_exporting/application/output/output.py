import logging

from deps_message_flow.events.publisher import DomainEventPublisher

from deps_output_exporting.constants import DOCUMENTS_EXCHANGER
from deps_output_exporting.domain.exceptions import DocumentTypeNotFound, OutputNotFound
from deps_output_exporting.domain.model import (
    DeleteFiles,
    DocumentType,
    IDocumentTypeRepository,
    IOutputRepository,
    Output,
    SchemaType,
)
from deps_output_exporting.infrastructure.services import OutputBuildingService

__all__ = ["OutputService"]


class OutputService:
    def __init__(
        self,
        document_type_repository: IDocumentTypeRepository,
        output_repository: IOutputRepository,
        output_building_service: OutputBuildingService,
        domain_event_publisher: DomainEventPublisher,
    ):
        self._document_type_repository = document_type_repository
        self._output_repository = output_repository
        self._output_building_service = output_building_service
        self._domain_event_publisher = domain_event_publisher

        self._logger = logging.getLogger(self.__class__.__name__)

    def create_empty_output(self, document_id: str, tenant_id: str, document_type_id: str, profile_id: str) -> Output:
        document_type = self._find_document_type(document_type_id, tenant_id)
        profile = document_type.get_profile(profile_id)
        empty_output = self._output_building_service.build_empty(
            document_id=document_id,
            tenant_id=tenant_id,
            profile=profile,
        )
        self._output_repository.save(empty_output)

        return empty_output

    def build_output(self, document_id: str, tenant_id: str, document_type_id: str, profile_id: str) -> Output:
        document_type = self._find_document_type(document_type_id, tenant_id)
        profile = document_type.get_profile(profile_id)
        new_output = self._output_building_service.build(document_id, tenant_id, profile, document_type_id)
        self._output_repository.save(new_output)

        deleted_outputs = self._output_repository.delete_outdated_outputs(document_id, tenant_id, profile_id)
        for output in deleted_outputs:
            self._send_event(output.document_id, output.file_path)

        return new_output

    def find_outputs_by_document_id(self, document_id: str, tenant_id: str) -> list[Output]:
        return self._output_repository.find_by_document_id(tenant_id, document_id)

    def delete_output(
        self,
        document_id: str,
        tenant_id: str,
        output_id: str,
    ) -> None:
        deleted_output = self._output_repository.delete(tenant_id, document_id, output_id)
        if deleted_output is not None:
            self._send_event(deleted_output.document_id, deleted_output.file_path)

    def delete_document_edata_outputs(self, document_id: str, tenant_id: str) -> None:
        document_outputs = self._output_repository.find_by_document_id(tenant_id, document_id)
        outputs_with_edata_schema = [
            output for output in document_outputs if output.profile_info.schema_type == SchemaType.EXTRACTED_DATA
        ]
        outputs_to_delete_ids = [output.id() for output in outputs_with_edata_schema]
        self._output_repository.delete_all(tenant_id, outputs_to_delete_ids)
        for output in outputs_with_edata_schema:
            self._send_event(output.document_id, output.file_path)

    def update_output(
        self,
        tenant_id: str,
        output_id: str,
        document_id: str,
        profile_id: str,
        new_file_path: str | None,
    ):
        output = self.find_output_by_id(output_id=output_id, tenant_id=tenant_id)
        output.assign_file(file_path=new_file_path)
        self._output_repository.save(output)
        self._output_repository.delete_outdated_outputs(
            tenant_id=tenant_id,
            document_id=document_id,
            profile_id=profile_id,
        )

    def find_output_by_id(self, output_id: str, tenant_id: str) -> Output:
        if output := self._output_repository.find_by_id(tenant_id=tenant_id, output_id=output_id):
            return output
        raise OutputNotFound(output_id)

    def _find_document_type(self, document_type_id: str, tenant_id: str) -> DocumentType:
        if (document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)) is None:
            raise DocumentTypeNotFound(document_type_id)
        return document_type

    def _send_event(self, document_id: str, file_path: str):
        self._domain_event_publisher.publish(
            DOCUMENTS_EXCHANGER,
            str(document_id),
            [DeleteFiles(file_paths=[file_path])],
        )
