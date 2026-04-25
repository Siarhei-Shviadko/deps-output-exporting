from typing import Any, Dict, Optional, Type, Union

from dependency_injector import containers, providers, resources
from deps_asb import ASBClient, ASBConsumer, ASBProducer
from deps_kafka import KafkaClient, KafkaConsumer, KafkaProducer
from deps_message_flow import MessagingDriverEnum
from deps_message_flow.commands.producer import CommandProducer
from deps_message_flow.events.publisher import DomainEventPublisher
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer
from deps_message_flow.sagas.orchestration import (
    SagaCommandProducer,
    SagaDataMapping,
    SagaInstanceFactory,
    SagaManagerFactory,
)
from deps_rabbitmq import RabbitMQClient, RabbitMQConsumer, RabbitMQProducer

from deps_output_exporting.application import (
    DocumentTypeService,
    DocumentTypeServiceWithSagas,
    OutputService,
    OutputServiceWithSagas,
    RoutingInfoService,
)
from deps_output_exporting.constants import PROJECT_NAME
from deps_output_exporting.domain.model import (
    Code,
    IDocumentTypeRepository,
    IOutputRepository,
    IRoutingInfoRepository,
    SchemaType,
)
from deps_output_exporting.extras.datasource import Database, DBDialect, DBDriver
from deps_output_exporting.infrastructure.access_management import user
from deps_output_exporting.infrastructure.external_storages import (
    OneDriveStorage,
    SalesforceStorage,
)
from deps_output_exporting.infrastructure.proxies import (
    DocumentProxy,
    DocumentTypeProxy,
    ExtractionProxy,
    FileStorageProxy,
    HighSparrowProxy,
    IValidationProxy,
    ParsingProxy,
    PrompterProxy,
    UnifierProxy,
    ValidationProxy,
)
from deps_output_exporting.infrastructure.repositories import (
    DocumentTypeRepository,
    OutputRepository,
    RoutingInfoRepository,
    SagaInstanceRepository,
)
from deps_output_exporting.infrastructure.services import (
    DLOutputGenerator,
    EdataOutputGenerator,
    OutputBuildingService,
)
from deps_output_exporting.messaging.dispatcher import make_message_dispatcher
from deps_output_exporting.messaging.sagas import (
    OutputCreationSaga,
    ProfileCreationSaga,
    ProfileDeletionSaga,
)
from deps_output_exporting.messaging.sagas.plugin_attachment import PluginAttachmentSaga
from deps_output_exporting.messaging.sagas_data import (
    OutputCreationSteps,
    PluginAttachmentSteps,
    ProfileCreationSteps,
    ProfileDeletionSteps,
    make_saga_data_mapping,
)

MessagingClient = Union[ASBClient, KafkaClient, RabbitMQClient]


class DatabaseResource(resources.Resource):
    def init(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        dialect: DBDialect,
        driver: DBDriver,
        require_secure_transport: bool,
    ) -> Database:
        db = Database(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            dialect=dialect,
            driver=driver,
            require_secure_transport=require_secure_transport,
        )
        db.connect()
        return db

    def shutdown(self, resource: Database) -> None:
        resource.close()


class MessageBrokerResource(resources.Resource):
    def init(
        self,
        driver_type: str,
        expected_driver: str,
        client: Type[MessagingClient],
        message_connection_string: str,
        **kwargs: Dict[str, Any],
    ) -> Optional[MessagingClient]:
        return client(message_connection_string, **kwargs) if driver_type == expected_driver else None

    def shutdown(self, resource: Optional[MessagingClient]) -> None:
        if resource:
            resource.close()


class MessageBrokers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)

    broker_client: providers.Provider[MessagingClient] = providers.Selector(
        config.messaging_driver,
        asb=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.ASB.value,
            expected_driver=config.messaging_driver,
            client=ASBClient,
            message_connection_string=config.message_broker_connection_string,
            asb_settings=messaging_driver_settings,
        ),
        kafka=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.KAFKA.value,
            expected_driver=config.messaging_driver,
            client=KafkaClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
        rabbitmq=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.RABBITMQ.value,
            expected_driver=config.messaging_driver,
            client=RabbitMQClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
    )


class Messaging(containers.DeclarativeContainer):
    config = providers.Configuration()
    message_brokers = providers.DependenciesContainer()

    producer: providers.Provider[IMessageProducer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBProducer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
        ),
        kafka=providers.Singleton(
            KafkaProducer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQProducer,
            client=message_brokers.broker_client,
        ),
    )
    consumer: providers.Provider[IMessageConsumer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBConsumer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
            custom_subscription_name=PROJECT_NAME,
        ),
        kafka=providers.Singleton(
            KafkaConsumer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQConsumer,
            client=message_brokers.broker_client,
        ),
    )


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    build_info: providers.Provider[Dict] = providers.Dict(
        {
            "build_tag": config.info.tag,
            "build_date": config.info.date,
            "commit_hash": config.info.hash,
        },
    )


class Datasources(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_datasource: providers.Provider[Database] = providers.Resource(
        DatabaseResource,
        config.user,
        config.password,
        config.host,
        config.port,
        config.db,
        config.dialect,
        config.driver,
        config.require_secure_transport,
    )


class Repositories(containers.DeclarativeContainer):
    datasources = providers.DependenciesContainer()
    document_type: providers.Singleton[IDocumentTypeRepository] = providers.Singleton(
        DocumentTypeRepository,
        database=datasources.postgres_datasource,
    )
    output: providers.Singleton[IOutputRepository] = providers.Singleton(
        OutputRepository,
        database=datasources.postgres_datasource,
    )
    routing_info: providers.Singleton[IRoutingInfoRepository] = providers.Singleton(
        RoutingInfoRepository,
        database=datasources.postgres_datasource,
    )
    saga_instance: providers.Provider[SagaInstanceRepository] = providers.Singleton(
        SagaInstanceRepository,
        datasources.postgres_datasource,
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    file_storage_proxy: providers.Provider[FileStorageProxy] = providers.Singleton(
        FileStorageProxy,
        base_url=config.file_storage.url,
        timeout=config.file_storage.timeout,
        ssl_verify=config.ssl_verify,
    )
    extraction_proxy: providers.Provider[ExtractionProxy] = providers.Singleton(
        ExtractionProxy,
        base_url=config.extraction.url,
        timeout=config.extraction.timeout,
        ssl_verify=config.ssl_verify,
    )
    document_type_proxy: providers.Provider[DocumentTypeProxy] = providers.Singleton(
        DocumentTypeProxy,
        base_url=config.document_type.url,
        timeout=config.document_type.timeout,
        ssl_verify=config.ssl_verify,
    )
    document_proxy: providers.Provider[DocumentProxy] = providers.Singleton(
        DocumentProxy,
        base_url=config.document.url,
        timeout=config.document.timeout,
        ssl_verify=config.ssl_verify,
    )
    unifier_proxy: providers.Provider[UnifierProxy] = providers.Singleton(
        UnifierProxy,
        base_url=config.unifier.url,
        timeout=config.unifier.timeout,
        ssl_verify=config.ssl_verify,
    )

    high_sparrow_proxy: providers.Provider[IValidationProxy] = providers.Singleton(
        HighSparrowProxy,
        base_url=config.high_sparrow.url,
        timeout=config.high_sparrow.timeout,
        ssl_verify=config.ssl_verify,
    )

    validation_proxy: providers.Provider[IValidationProxy] = providers.Singleton(
        ValidationProxy,
        base_url=config.validation.url,
        timeout=config.validation.timeout,
        ssl_verify=config.ssl_verify,
    )

    parsing_proxy: providers.Provider[ParsingProxy] = providers.Singleton(
        ParsingProxy,
        base_url=config.parsing.url,
        timeout=config.parsing.timeout,
        ssl_verify=config.ssl_verify,
    )
    prompter_proxy: providers.Provider[PrompterProxy] = providers.Singleton(
        PrompterProxy,
        base_url=config.prompter.url,
        timeout=config.prompter.timeout,
        ssl_verify=config.ssl_verify,
    )
    one_drive: providers.Provider[OneDriveStorage] = providers.Singleton(
        OneDriveStorage,
        scopes=config.one_drive.scopes,
        base_url=config.one_drive.base_url,
        authority_prefix=config.one_drive.authority_prefix,
    )
    salesforce: providers.Provider[SalesforceStorage] = providers.Singleton(
        SalesforceStorage,
        base_url=config.salesforce.base_url,
        auth_endpoint=config.salesforce.auth_endpoint,
        upload_endpoint=config.salesforce.upload_endpoint,
    )


class SagaSteps(containers.DeclarativeContainer):
    document_type_service: providers.Dependency[DocumentTypeService] = providers.Dependency()
    output_service: providers.Dependency[OutputService] = providers.Dependency()
    routing_info_service: providers.Dependency[RoutingInfoService] = providers.Dependency()
    document_type_proxy: providers.Dependency[DocumentTypeProxy] = providers.Dependency()

    profile_creation: providers.Singleton[ProfileCreationSteps] = providers.Singleton(
        ProfileCreationSteps,
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
    )
    profile_deletion: providers.Singleton[ProfileDeletionSteps] = providers.Singleton(
        ProfileDeletionSteps,
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
    )
    plugin_attachment: providers.Singleton[PluginAttachmentSteps] = providers.Singleton(
        PluginAttachmentSteps,
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
        document_type_proxy=document_type_proxy,
    )
    output_creation: providers.Singleton[OutputCreationSteps] = providers.Singleton(
        OutputCreationSteps,
        output_service=output_service,
        routing_info_service=routing_info_service,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)
    current_user_tenant = providers.Callable(lambda: user.get()["organisation"])

    datasources: providers.Container[Datasources] = providers.Container(
        Datasources,
        config=config.database,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        datasources=datasources,
    )

    core: providers.Container[Core] = providers.Container(Core, config=config)
    message_brokers: providers.Container[MessageBrokers] = providers.Container(
        MessageBrokers,
        config=config,
        messaging_driver_settings=messaging_driver_settings,
    )

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
        message_brokers=message_brokers,
    )

    command_producer: providers.Singleton[CommandProducer] = providers.Singleton(
        CommandProducer,
        messaging.producer,
    )

    domain_event_publisher: providers.Singleton[DomainEventPublisher] = providers.Singleton(
        DomainEventPublisher,
        messaging.producer,
    )

    document_type_service: providers.Singleton[DocumentTypeService] = providers.Singleton(
        DocumentTypeService,
        command_producer=command_producer,
        domain_event_publisher=domain_event_publisher,
        document_type_repository=repositories.document_type,
    )

    routing_info_service: providers.Singleton[RoutingInfoService] = providers.Singleton(
        RoutingInfoService,
        document_type_repository=repositories.document_type,
        routing_info_repository=repositories.routing_info,
    )

    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices,
        config=config,
    )
    edata_output_generator: providers.Singleton[EdataOutputGenerator] = providers.Singleton(
        EdataOutputGenerator,
        extraction=external_services.extraction_proxy,
        document_type=external_services.document_type_proxy,
        document=external_services.document_proxy,
        unifier=external_services.unifier_proxy,
        validation=external_services.validation_proxy,
        high_sparrow=external_services.high_sparrow_proxy,
        new_validation_process=config.new_validation_process,
    )

    dl_output_generator: providers.Singleton[DLOutputGenerator] = providers.Singleton(
        DLOutputGenerator,
        parsing=external_services.parsing_proxy,
        prompter=external_services.prompter_proxy,
        document_type=external_services.document_type_proxy,
        document=external_services.document_proxy,
        kvs_output_enabled=config.kvs_output_enabled,
    )

    output_building_service: providers.Singleton[OutputBuildingService] = providers.Singleton(
        OutputBuildingService,
        file_storage=external_services.file_storage_proxy,
        output_generators=providers.Dict(
            {
                SchemaType.EXTRACTED_DATA: edata_output_generator,
                SchemaType.DOCUMENT_LAYOUT: dl_output_generator,
            },
        ),
        external_storages=providers.Dict(
            {
                Code.ONE_DRIVE: external_services.one_drive,
                Code.SALESFORCE: external_services.salesforce,
            },
        ),
    )

    output_service: providers.Singleton[OutputService] = providers.Singleton(
        OutputService,
        document_type_repository=repositories.document_type,
        output_repository=repositories.output,
        output_building_service=output_building_service,
        domain_event_publisher=domain_event_publisher,
    )

    saga_steps: providers.Container[SagaSteps] = providers.Container(
        SagaSteps,
        document_type_service=document_type_service,
        routing_info_service=routing_info_service,
        document_type_proxy=external_services.document_type_proxy,
        output_service=output_service,
    )

    sagas = providers.List(
        providers.Singleton(ProfileCreationSaga, steps=saga_steps.profile_creation),
        providers.Singleton(ProfileDeletionSaga, steps=saga_steps.profile_deletion),
        providers.Singleton(PluginAttachmentSaga, steps=saga_steps.plugin_attachment),
        providers.Singleton(OutputCreationSaga, steps=saga_steps.output_creation, message_producer=messaging.producer),
    )

    saga_command_producer: providers.Singleton[CommandProducer] = providers.Singleton(
        SagaCommandProducer,
        command_producer,
    )

    saga_data_mapping: providers.Singleton[SagaDataMapping] = providers.Singleton(
        make_saga_data_mapping,
    )

    saga_manager_factory: providers.Singleton[SagaManagerFactory] = providers.Singleton(
        SagaManagerFactory,
        repositories.saga_instance,
        command_producer,
        messaging.consumer,
        saga_command_producer,
        saga_data_mapping,
    )

    saga_instance_factory: providers.Singleton[SagaManagerFactory] = providers.Singleton(
        SagaInstanceFactory,
        saga_manager_factory,
        sagas,
    )

    document_type_service_with_sagas: providers.Singleton[DocumentTypeServiceWithSagas] = providers.Singleton(
        DocumentTypeServiceWithSagas,
        saga_instance_factory=saga_instance_factory,
        sagas=sagas,
    )

    message_dispatcher: providers.Singleton[IMessageConsumer] = providers.Singleton(
        make_message_dispatcher,
        messaging.consumer,
        messaging.producer,
    )

    output_service_with_sagas: providers.Singleton[OutputServiceWithSagas] = providers.Singleton(
        OutputServiceWithSagas,
        saga_instance_factory=saga_instance_factory,
        sagas=sagas,
        document_type_repository=repositories.document_type,
        output_building_service=output_building_service,
        output_repository=repositories.output,
        domain_event_publisher=domain_event_publisher,
    )
