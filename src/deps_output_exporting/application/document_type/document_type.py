import logging
from typing import Optional

from deps_message_flow.commands.producer import CommandProducer
from deps_message_flow.events.publisher import DomainEventPublisher

from deps_output_exporting.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_output_exporting.domain.exceptions import DocumentTypeNotFound
from deps_output_exporting.domain.model import (
    DocumentType,
    DocumentTypeData,
    DocumentTypeFactory,
    EntityId,
    ExternalStorageInfoData,
    Format,
    GetDocumentTypes,
    IDocumentTypeRepository,
    Profile,
    SchemaData,
)

__all__ = ["DocumentTypeService"]


class DocumentTypeService:
    def __init__(
        self,
        command_producer: CommandProducer,
        domain_event_publisher: DomainEventPublisher,
        document_type_repository: IDocumentTypeRepository,
    ):
        self._command_producer = command_producer
        self._document_type_repository = document_type_repository
        self._domain_event_publisher = domain_event_publisher
        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        self._command_producer.send(
            COMMANDS_CHANNEL,
            GetDocumentTypes(),
            COMMANDS_REPLIES_CHANNEL,
        )
        self._logger.info("Command GetDocumentTypes sent")

    def find_document_type(self, document_type_id: str, tenant_id: str) -> DocumentType:
        if (document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)) is None:
            raise DocumentTypeNotFound(document_type_id)

        return document_type

    def save_document_type(
        self,
        document_type_id: str,
        tenant_id: str,
    ) -> None:
        document_type = DocumentTypeFactory.create(id_=document_type_id, tenant_id=tenant_id)
        self._document_type_repository.save(document_type)

    def save_document_types(self, document_types_data: list[DocumentTypeData]) -> None:
        self._document_type_repository.save_all(
            [
                DocumentTypeFactory.create(id_=dt["document_type_id"], tenant_id=dt["tenant_id"])
                for dt in document_types_data
            ],
        )

    def delete_document_type(self, document_type_id: str, tenant_id: str) -> None:
        self._document_type_repository.delete(document_type_id, tenant_id)

    def create_profile(
        self,
        document_type_id: str,
        tenant_id: str,
        name: str,
        schema: SchemaData,
        format_: str,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> EntityId:
        document_type = self.find_document_type(document_type_id, tenant_id)
        profile_id = document_type.add_profile(
            name=name,
            schema=schema,
            format_=format_,
            external_storages_info=external_storages_info,
        )
        self._document_type_repository.update(document_type)
        return profile_id

    def update_profile(
        self,
        document_type_id: str,
        tenant_id: str,
        profile_id: str,
        name: str,
        schema: SchemaData,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> EntityId:
        document_type = self.find_document_type(document_type_id, tenant_id)
        updated_profile_id = document_type.update_profile(
            profile_id,
            name,
            schema,
            external_storages_info,
        )
        self._document_type_repository.update(document_type)
        return updated_profile_id

    def delete_profile(self, document_type_id: str, tenant_id: str, profile_id: str) -> None:
        document_type = self.find_document_type(document_type_id, tenant_id)
        document_type.delete_profile(profile_id)
        self._document_type_repository.update(document_type)

    def find_profiles(self, document_type_id: str, tenant_id: str) -> list[Profile]:
        document_type = self.find_document_type(document_type_id, tenant_id)
        return list(document_type.profiles.values())

    def add_plugin_profile(
        self,
        profile_id: str,
        document_type_id: str,
        tenant_id: str,
        plugin_name: str,
        plugin_format: str,
        schema_data: SchemaData | None,
    ) -> None:
        try:
            document_type = self.find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        except DocumentTypeNotFound:
            document_type = DocumentTypeFactory.create(
                id_=document_type_id,
                tenant_id=tenant_id,
                create_default_profile=False,
            )
        document_type.add_plugin_profile(
            profile_id=profile_id,
            name=plugin_name,
            format_=plugin_format,
            schema_data=schema_data,
        )
        self._document_type_repository.update(document_type)
