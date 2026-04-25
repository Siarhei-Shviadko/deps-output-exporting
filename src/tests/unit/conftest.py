from collections import namedtuple
from datetime import datetime, timezone
from random import choice
from uuid import uuid4

import pytest
from faker import Faker

from deps_output_exporting.api import auth
from deps_output_exporting.domain.model import (
    Code,
    DocumentLayoutSchema,
    DocumentType,
    DocumentTypeFactory,
    EntityId,
    ExportingType,
    ExternalStorageInfo,
    ExternalStorageInfoData,
    ExtractedDataSchema,
    Format,
    OneDriveCredentials,
    OneDriveCredentialsData,
    Output,
    OutputState,
    ParsingFeature,
    ParsingType,
    Profile,
    ProfileInfo,
    SalesforceCredentials,
    SalesforceCredentialsData,
    SchemaData,
    SchemaType,
    TenantId,
)
from deps_output_exporting.infrastructure.access_management import user
from deps_output_exporting.infrastructure.proxies import (
    DocumentLayout,
    SerializedDocumentLayout,
)
from tests.data import document_layout_dict
from tests.fakes import (
    FakeCommandProducer,
    FakeDocumentProxy,
    FakeDocumentTypeProxy,
    FakeDocumentTypeRepo,
    FakeExtractionProxy,
    FakeFileStorageProxy,
    FakeMessageProducer,
    FakeOutputRepository,
    FakeRoutingInfoRepository,
    FakeSagaInstanceRepository,
    FakeSalesforceStorage,
    FakeUnifierProxy,
    FakeValidationProxy,
)

fake = Faker()


@pytest.fixture
def document_id(faker):
    return str(faker.random_int())


@pytest.fixture
def postgres_datasource_mock(mocker, containers):
    mock = mocker.Mock(containers.datasources.postgres_datasource())
    containers.datasources.postgres_datasource.override(mock)

    yield mock

    containers.datasources.reset_override()


@pytest.fixture(autouse=True)
def fake_document_type_repository(containers):
    with containers.repositories.document_type.override(FakeDocumentTypeRepo()):
        yield containers.repositories.document_type()


@pytest.fixture
def fake_command_producer(containers):
    with containers.command_producer.override(FakeCommandProducer()):
        yield containers.command_producer()


@pytest.fixture(autouse=True)
def fake_routing_info_repository(containers):
    with containers.repositories.routing_info.override(FakeRoutingInfoRepository()):
        yield containers.repositories.routing_info()


@pytest.fixture(autouse=True)
def fake_saga_instance_repository(containers):
    with containers.repositories.saga_instance.override(FakeSagaInstanceRepository()) as dep:
        yield dep()


@pytest.fixture
def fake_document_proxy(external_services):
    with external_services.document_proxy.override(FakeDocumentProxy()) as dp:
        yield dp()


@pytest.fixture
def fake_extraction_proxy(external_services):
    with external_services.extraction_proxy.override(FakeExtractionProxy()) as ep:
        yield ep()


@pytest.fixture
def fake_document_type_proxy(external_services):
    with external_services.document_type_proxy.override(FakeDocumentTypeProxy()) as dtp:
        yield dtp()


@pytest.fixture
def fake_unifier_proxy(external_services):
    with external_services.unifier_proxy.override(FakeUnifierProxy()) as up:
        yield up()


@pytest.fixture
def fake_validation_proxy(external_services):
    with external_services.validation_proxy.override(FakeValidationProxy()) as vp:
        yield vp()


@pytest.fixture
def fake_file_storage_proxy(external_services):
    with external_services.file_storage_proxy.override(FakeFileStorageProxy()) as fsp:
        yield fsp()


@pytest.fixture
def fake_salesforce_storage(external_services):
    with external_services.salesforce.override(FakeSalesforceStorage()) as ss:
        yield ss()


@pytest.fixture
def fake_message_producer():
    return FakeMessageProducer()


@pytest.fixture
def document_type_service(containers, fake_document_type_repository, fake_command_producer):
    yield containers.document_type_service()


@pytest.fixture
def routing_info_service(containers, fake_routing_info_repository):
    yield containers.routing_info_service()


@pytest.fixture
def test_tenant_id():
    return uuid4().hex


@pytest.fixture
def this_user(test_tenant_id):
    return dict(
        subject="Tiger",
        groups=[test_tenant_id],
        token="token",
        roles=[],
        organisation=test_tenant_id,
    )


@pytest.fixture(autouse=True)
def set_this_user(this_user):
    user.set(this_user)


@pytest.fixture(autouse=True)
def mocked_middleware(monkeypatch, mocker):
    monkeypatch.setattr(auth, "set_user_from_token", mocker.Mock({}))


@pytest.fixture
def enable_key_values_output(containers):
    with containers.config.kvs_output_enabled.override(True):
        yield


@pytest.fixture
def profile_id():
    return uuid4().hex


@pytest.fixture
def profile_name(faker) -> str:
    return faker.name()


@pytest.fixture
def onedrive_storage(containers):
    return containers.external_services.one_drive()


@pytest.fixture
def onedrive_client_id():
    return uuid4().hex


@pytest.fixture
def onedrive_secret():
    return uuid4().hex


@pytest.fixture
def onedrive_tenant_id():
    return uuid4().hex


@pytest.fixture
def onedrive_user_id():
    return uuid4().hex


@pytest.fixture
def profile_one_drive_credentials(
    onedrive_client_id, onedrive_secret, onedrive_tenant_id, onedrive_user_id
) -> OneDriveCredentials:
    return OneDriveCredentials(
        client_id=onedrive_client_id,
        secret=onedrive_secret,
        tenant_id=onedrive_tenant_id,
        user_id=onedrive_user_id,
    )


@pytest.fixture
def salesforce_storage(containers):
    return containers.external_services.salesforce()


@pytest.fixture
def salesforce_client_id():
    return uuid4().hex


@pytest.fixture
def salesforce_client_secret():
    return uuid4().hex


@pytest.fixture
def salesforce_owner_id():
    return uuid4().hex


@pytest.fixture
def salesforce_location_id():
    return uuid4().hex


@pytest.fixture
def profile_salesforce_credentials(
    salesforce_client_id,
    salesforce_client_secret,
    salesforce_owner_id,
    salesforce_location_id,
) -> SalesforceCredentials:
    return SalesforceCredentials(
        client_id=salesforce_client_id,
        client_secret=salesforce_client_secret,
        owner_id=salesforce_owner_id,
        location_id=salesforce_location_id,
    )


@pytest.fixture
def external_storages_info_with_one_drive_credentials(profile_one_drive_credentials) -> list[ExternalStorageInfo]:
    return [
        ExternalStorageInfo(
            code=Code.ONE_DRIVE,
            credentials=profile_one_drive_credentials,
            output_directory_path=fake.uri_path(),
        )
    ]


@pytest.fixture
def external_storages_info_with_salesforce_credentials(profile_salesforce_credentials) -> list[ExternalStorageInfo]:
    return [
        ExternalStorageInfo(
            code=Code.SALESFORCE,
            credentials=profile_salesforce_credentials,
            output_directory_path=fake.uri_path(),
        )
    ]


@pytest.fixture
def profile_extracted_data_schema(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["field1", "field2", "field3"],
            needs_validation_results=True,
        ),
        version=uuid4().hex,
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def profile_document_layout_schema(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=DocumentLayoutSchema(parsing_type=ParsingType.TESSERACT, features=list(ParsingFeature)),
        version=uuid4().hex,
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def doc_type_two_types_of_profile(
    profile_extracted_data_schema,
    profile_document_layout_schema,
    test_tenant_id,
    document_type_id,
):
    return DocumentType(
        id_=EntityId(document_type_id),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile_extracted_data_schema.id(): profile_extracted_data_schema,
            profile_document_layout_schema.id(): profile_document_layout_schema,
        },
    )


@pytest.fixture
def test_document_type_row():
    """
    The SQLAlchemy `Row` object seeks to act as much like a Python named tuple as possible.
    """
    yield namedtuple(
        "TestDocTypeRow",
        [
            "id",
            "tenant_id",
            "profiles",
        ],
    )


@pytest.fixture
def fake_output_repository(containers):
    with containers.repositories.output.override(FakeOutputRepository()):
        yield containers.repositories.output()


@pytest.fixture
def output_service(containers, fake_document_type_repository, fake_output_repository):
    yield containers.output_service()


@pytest.fixture
def output_service_with_sagas(containers, fake_document_type_repository, fake_output_repository):
    yield containers.output_service_with_sagas()


@pytest.fixture
def output_building_service(containers):
    yield containers.output_building_service()


@pytest.fixture
def profile_format() -> Format:
    return choice([Format("json"), Format("excel")])


@pytest.fixture
def profile_info():
    return ProfileInfo(
        id_=EntityId(uuid4().hex),
        version=uuid4().hex,
        schema_type=choice(list(SchemaType)),
    )


@pytest.fixture
def output(profile_info, test_tenant_id, document_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info,
        document_id=document_id,
        state=choice([OutputState.READY, OutputState.PENDING]),
        file_path=faker.file_path(),
    )


@pytest.fixture
def profile_info_edata_schema():
    return ProfileInfo(
        id_=EntityId(uuid4().hex),
        version=uuid4().hex,
        schema_type=SchemaType.EXTRACTED_DATA,
    )


@pytest.fixture
def output_edata_schema(profile_info_edata_schema, test_tenant_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info_edata_schema,
        document_id=str(faker.random_int()),
        state=choice(list(OutputState)),
        file_path=faker.file_path(),
    )


@pytest.fixture
def profile_info_dl_schema():
    return ProfileInfo(
        id_=EntityId(uuid4().hex),
        version=uuid4().hex,
        schema_type=SchemaType.DOCUMENT_LAYOUT,
    )


@pytest.fixture
def output_dl_schema(profile_info_dl_schema, test_tenant_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info_dl_schema,
        document_id=str(faker.random_int()),
        state=choice(list(OutputState)),
        file_path=faker.file_path(),
    )


@pytest.fixture(scope="function", autouse=True)
def domain_event_publisher(containers, mocker):
    containers.domain_event_publisher.override(mocker.Mock(containers.domain_event_publisher.cls))
    yield containers.domain_event_publisher()
    containers.domain_event_publisher.reset_override()


@pytest.fixture
def profile_extracted_data_schema_with_external_storages_info(
    external_storages_info_with_salesforce_credentials,
    profile_entity_id,
    faker,
):
    return Profile(
        id_=profile_entity_id,
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["field1", "field2", "field3"],
            needs_validation_results=True,
        ),
        version=uuid4().hex,
        external_storages_info=external_storages_info_with_salesforce_credentials,
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def profile_document_layout_schema_with_external_storages_info(
    external_storages_info_with_one_drive_credentials, faker
):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=DocumentLayoutSchema(parsing_type=ParsingType.TESSERACT, features=list(ParsingFeature)),
        version=uuid4().hex,
        external_storages_info=external_storages_info_with_one_drive_credentials,
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def doc_type_two_types_of_profile_with_external_storages_info(
    profile_extracted_data_schema_with_external_storages_info,
    profile_document_layout_schema_with_external_storages_info,
    test_tenant_id,
    document_type_id,
):
    profile_extracted_data = profile_extracted_data_schema_with_external_storages_info
    profile_document_layout = profile_document_layout_schema_with_external_storages_info
    return DocumentType(
        id_=EntityId(document_type_id),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile_extracted_data.id(): profile_extracted_data,
            profile_document_layout.id(): profile_document_layout,
        },
    )


@pytest.fixture
def save_doc_type_two_types_of_profile_with_external_storages_info(
    doc_type_two_types_of_profile_with_external_storages_info,
    fake_document_type_repository,
):
    fake_document_type_repository.save(doc_type_two_types_of_profile_with_external_storages_info)


@pytest.fixture
def document_layout() -> DocumentLayout:
    return SerializedDocumentLayout.model_validate(document_layout_dict).to_model()


@pytest.fixture
def document_type_id():
    return uuid4().hex


@pytest.fixture
def document_type(document_type_id, test_tenant_id):
    return DocumentTypeFactory.create(document_type_id, test_tenant_id)


@pytest.fixture
def extracted_data_schema(faker) -> ExtractedDataSchema:
    return ExtractedDataSchema(fields=[faker.word(), faker.word()], needs_validation_results=faker.boolean())


@pytest.fixture
def document_layout_schema() -> DocumentLayoutSchema:
    return DocumentLayoutSchema(parsing_type=ParsingType.TESSERACT, features=list(ParsingFeature))


@pytest.fixture
def profile_creation_date(faker) -> datetime:
    return faker.date_time_between(start_date="-1y", end_date="now")


@pytest.fixture
def profile_schema(extracted_data_schema, document_layout_schema):
    return choice([extracted_data_schema, document_layout_schema])


@pytest.fixture
def profile_version():
    return uuid4().hex


@pytest.fixture
def profile_entity_id(profile_id):
    return EntityId(profile_id)


@pytest.fixture
def profile(profile_entity_id, profile_creation_date, profile_name, profile_schema, profile_version):
    return Profile(
        id_=profile_entity_id,
        creation_date=profile_creation_date,
        name=profile_name,
        schema=profile_schema,
        version=profile_version,
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def extracted_data_schema_data(extracted_data_schema) -> SchemaData:
    return SchemaData(
        fields=extracted_data_schema.fields, needs_validation_results=extracted_data_schema.needs_validation_results
    )


@pytest.fixture
def document_layout_schema_data(document_layout_schema) -> SchemaData:
    return SchemaData(parsing_type=document_layout_schema.parsing_type, features=document_layout_schema.features)


@pytest.fixture
def profile_schema_data(profile_schema, extracted_data_schema_data, document_layout_schema_data):
    class_to_fixture = {
        DocumentLayoutSchema: document_layout_schema_data,
        ExtractedDataSchema: extracted_data_schema_data,
    }
    return class_to_fixture[type(profile_schema)]


@pytest.fixture
def new_extracted_data_schema(faker) -> ExtractedDataSchema:
    return ExtractedDataSchema(fields=[faker.word(), faker.word()], needs_validation_results=faker.boolean())


@pytest.fixture
def new_extracted_data_schema_data(new_extracted_data_schema) -> SchemaData:
    return SchemaData(
        fields=new_extracted_data_schema.fields,
        needs_validation_results=new_extracted_data_schema.needs_validation_results,
    )


@pytest.fixture
def profile_one_drive_credentials_data() -> OneDriveCredentialsData:
    return OneDriveCredentialsData(
        client_id=uuid4().hex,
        secret=uuid4().hex,
        tenant_id=uuid4().hex,
        user_id=uuid4().hex,
    )


@pytest.fixture
def profile_salesforce_credentials_data() -> SalesforceCredentialsData:
    return SalesforceCredentialsData(
        client_id=uuid4().hex,
        client_secret=uuid4().hex,
        owner_id=uuid4().hex,
        location_id=uuid4().hex,
    )


@pytest.fixture
def external_storages_info_schema_data(
    profile_salesforce_credentials_data,
    profile_one_drive_credentials_data,
) -> list[ExternalStorageInfoData]:
    return [
        ExternalStorageInfoData(
            code=Code.SALESFORCE,
            credentials=profile_salesforce_credentials_data,
            output_directory_path=fake.uri_path(),
        ),
        ExternalStorageInfoData(
            code=Code.ONE_DRIVE,
            credentials=profile_one_drive_credentials_data,
            output_directory_path=fake.uri_path(),
        ),
    ]


@pytest.fixture
def output_creation_service(containers, fake_file_storage_proxy):
    yield containers.output_building_service()


@pytest.fixture
def empty_output(profile_info, test_tenant_id, document_id):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info,
        document_id=document_id,
        state=OutputState.PENDING,
        file_path=None,
    )
