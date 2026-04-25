from typing import Any

from deps_asb import ASBSettings
from deps_kafka import KafkaSettings
from deps_message_flow import MessagingDriverEnum
from deps_rabbitmq import RabbitMQTLSSettings
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from deps_output_exporting.extras.datasource import DatabaseSettings
from deps_output_exporting.extras.settings import (
    AuthenticationSettings,
    ServiceInfoSettings,
)


class FileStorageProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="FILE_STORAGE_")


class ExtractionProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="EXTRACTION_")


class DocumentTypeProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="DOCUMENT_TYPE_")


class DocumentProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="DOCUMENT_")


class UnifierProxySettings(BaseSettings):
    url: str
    timeout: int = 120

    model_config = SettingsConfigDict(env_prefix="UNIFIER_")


class ValidationProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="VALIDATION_")


class HighSparrowProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="HIGH_SPARROW_")


class ParsingProxySettings(BaseSettings):
    url: str
    timeout: int = 120

    model_config = SettingsConfigDict(env_prefix="PARSING_")


class PrompterProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="PROMPTER_")


class OneDriveStorageSettings(BaseSettings):
    scopes: list[str]
    base_url: str
    authority_prefix: str

    model_config = SettingsConfigDict(env_prefix="ONE_DRIVE_")


class SalesforceSettings(BaseSettings):
    base_url: str
    auth_endpoint: str
    upload_endpoint: str

    model_config = SettingsConfigDict(env_prefix="SALESFORCE_")


class Settings(BaseSettings):
    env: str = "development"
    version: str = "1.0"

    logger_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    info: ServiceInfoSettings = ServiceInfoSettings()
    database: DatabaseSettings = DatabaseSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()

    messaging_driver: MessagingDriverEnum = Field(MessagingDriverEnum.RABBITMQ, validation_alias="MESSAGING_DRIVER")
    messaging_driver_settings: Any = Field(None, validation_alias="MESSAGING_DRIVER_SETTINGS")
    message_broker_connection_string: str

    documentation_enabled: bool = True

    file_storage: FileStorageProxySettings = FileStorageProxySettings()
    extraction: ExtractionProxySettings = ExtractionProxySettings()
    document_type: DocumentTypeProxySettings = DocumentTypeProxySettings()
    document: DocumentProxySettings = DocumentProxySettings()
    unifier: UnifierProxySettings = UnifierProxySettings()
    validation: ValidationProxySettings = ValidationProxySettings()
    high_sparrow: HighSparrowProxySettings = HighSparrowProxySettings()
    parsing: ParsingProxySettings = ParsingProxySettings()
    prompter: PrompterProxySettings = PrompterProxySettings()

    one_drive: OneDriveStorageSettings = OneDriveStorageSettings()
    salesforce: SalesforceSettings = SalesforceSettings()

    new_validation_process: bool = False

    ssl_verify: bool = False
    kvs_output_enabled: bool = False

    instrumentation_enabled: bool = False

    model_config = SettingsConfigDict(use_enum_values=True)

    @field_validator("messaging_driver_settings")
    @classmethod
    def validate_messaging_driver_settings(cls, v, values):  # noqa: N805
        messaging_driver = values.data.get("messaging_driver")
        if not messaging_driver:
            raise ValueError("Invalid messaging driver")

        driver = MessagingDriverEnum(messaging_driver)
        if driver == MessagingDriverEnum.ASB:
            return ASBSettings()
        elif driver == MessagingDriverEnum.KAFKA:
            return KafkaSettings()
        elif driver == MessagingDriverEnum.RABBITMQ:
            return RabbitMQTLSSettings().dict()  # TODO: use BaseSettings

        raise ValueError(f"Driver {driver} is not implemented")
