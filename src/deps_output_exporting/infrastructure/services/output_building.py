import logging
from uuid import uuid4

from deps_output_exporting.domain.model import (
    Code,
    DocumentLayoutSchema,
    ExternalStorageInfo,
    ExtractedDataSchema,
    Format,
    Output,
    OutputBuilder,
    Profile,
    Schema,
    SchemaType,
)
from deps_output_exporting.infrastructure.external_storages import ExternalStorage
from deps_output_exporting.infrastructure.proxies import FileStorageProxy

from .output_generator import OutputGenerator

__all__ = ["OutputBuildingService"]


class OutputBuildingService:
    FILEPATH = "output/"

    def __init__(
        self,
        file_storage: FileStorageProxy,
        output_generators: dict[SchemaType, OutputGenerator],
        external_storages: dict[Code, ExternalStorage],
    ):
        self._file_storage: FileStorageProxy = file_storage
        self._output_generators = output_generators
        self._external_storages = external_storages

        self.extension_mapping = {
            Format("json"): "json",
            Format("excel"): "xlsx",
        }
        self._schema_mapping = {
            type(None): None,
            DocumentLayoutSchema: SchemaType.DOCUMENT_LAYOUT,
            ExtractedDataSchema: SchemaType.EXTRACTED_DATA,
        }

        self._logger = logging.getLogger(self.__class__.__name__)

    def build_empty(self, document_id: str, tenant_id: str, profile: Profile):
        schema_type = self._get_schema_type(profile.schema)
        return (
            OutputBuilder.for_document_id(document_id)
            .for_tenant(tenant_id)
            .with_profile_info(profile.id, profile.version, schema_type)
            .without_file_path()
            .build()
        )

    def build(self, document_id: str, tenant_id: str, profile: Profile, document_type_id: str) -> Output:
        schema_type = self._get_schema_type(profile.schema)
        output_file = self._generate_output_file(schema_type, profile, document_id, document_type_id)
        file_path = self._upload_output(profile, output_file)

        return (
            OutputBuilder.for_document_id(document_id)
            .for_tenant(tenant_id)
            .with_profile_info(profile.id, profile.version, schema_type)
            .with_file_path(file_path)
            .build()
        )

    def _upload_output(self, profile: Profile, output_file: bytes) -> str:
        file_name = self._generate_file_name(profile.format)
        file_path = self._upload_file_to_storage(file_name, output_file)
        self._logger.info("Output file was uploaded to file storage")

        if external_storages_info := profile.external_storages_info:
            self._upload_file_to_external_storages(external_storages_info, file_name, output_file)

        return file_path

    def _generate_output_file(self, schema_type: SchemaType, profile: Profile, document_id: str, document_type_id: str):
        return self._output_generators[schema_type].generate(
            document_id=document_id,
            profile=profile,
            document_type_id=document_type_id,
        )

    def _upload_file_to_storage(self, file_name: str, output_file: bytes) -> str:
        return self._file_storage.upload_file(self.FILEPATH, file_name, output_file)

    def _generate_file_name(self, format_: Format) -> str:
        name = uuid4().hex
        extension = self.extension_mapping.get(format_, format_())
        return f"{name}.{extension}"

    def _get_schema_type(self, profile_schema: Schema) -> SchemaType | None:
        try:
            return self._schema_mapping[type(profile_schema)]
        except KeyError:
            raise RuntimeError(f"No schema type for {profile_schema}")

    def _upload_file_to_external_storages(
        self,
        external_storages_info: list[ExternalStorageInfo],
        file_name: str,
        output_file: bytes,
    ) -> None:
        for storage_info in external_storages_info:
            if (storage_service := self._external_storages.get(storage_info.code)) is not None:
                storage_service.upload(file_name, output_file, storage_info)
                self._logger.info("Output file was uploaded to %s storage", storage_info.code.value)
            else:
                self._logger.error("Service for %s storage is not implemented", storage_info.code.value)
