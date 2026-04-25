from random import choice
from uuid import uuid4

import pytest
from faker import Faker

from deps_output_exporting.api import (
    BuildOutputRequest,
    CreateProfileRequest,
    SaveProfileRequest,
    SerializedDocumentLayoutSchema,
    SerializedExternalStorageInfo,
    SerializedExtractedDataSchema,
    SerializedOneDriveCredentials,
    SerializedSalesforceCredentials,
)
from deps_output_exporting.domain.model import (
    Code,
    DocumentTypeFactory,
    EntityId,
    Output,
    OutputState,
    ParsingFeature,
    ParsingType,
    ProfileInfo,
    SchemaData,
    SchemaType,
    TenantId,
)

fake = Faker()


@pytest.fixture
def extracted_data_schema(faker) -> SerializedExtractedDataSchema:
    return SerializedExtractedDataSchema(fields=[faker.word(), faker.word()], needs_validation_results=faker.boolean())


@pytest.fixture
def document_layout_schema() -> SerializedDocumentLayoutSchema:
    return SerializedDocumentLayoutSchema(parsing_type=ParsingType.TESSERACT, features=list(ParsingFeature))


@pytest.fixture
def profile_request_model(extracted_data_schema, document_layout_schema, faker) -> SaveProfileRequest:
    schema = choice([extracted_data_schema, document_layout_schema])

    return SaveProfileRequest(
        name=faker.name(),
        schema_=schema,
    )


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
def serialized_profile_one_drive_credentials(
    onedrive_client_id, onedrive_secret, onedrive_tenant_id, onedrive_user_id
) -> SerializedOneDriveCredentials:
    return SerializedOneDriveCredentials(
        client_id=onedrive_client_id,
        secret=onedrive_secret,
        tenant_id=onedrive_tenant_id,
        user_id=onedrive_user_id,
    )


@pytest.fixture
def serialized_profile_salesforce_credentials(
    salesforce_client_id, salesforce_client_secret, salesforce_owner_id, salesforce_location_id
) -> SerializedSalesforceCredentials:
    return SerializedSalesforceCredentials(
        client_id=salesforce_client_id,
        client_secret=salesforce_client_secret,
        owner_id=salesforce_owner_id,
        location_id=salesforce_location_id,
    )


@pytest.fixture
def profile_external_storages_info(
    faker,
    serialized_profile_salesforce_credentials,
    serialized_profile_one_drive_credentials,
) -> list[SerializedExternalStorageInfo]:
    external_storages_info_salesforce = SerializedExternalStorageInfo(
        code=Code.SALESFORCE.value,
        credentials=serialized_profile_salesforce_credentials,
        output_directory_path=fake.uri_path(),
    )
    external_storages_info_one_drive = SerializedExternalStorageInfo(
        code=Code.ONE_DRIVE.value,
        credentials=serialized_profile_one_drive_credentials,
        output_directory_path=fake.uri_path(),
    )
    return [
        external_storages_info_salesforce,
        external_storages_info_one_drive,
    ]


@pytest.fixture
def create_profile_request_model_with_schema(
    extracted_data_schema,
    document_layout_schema,
    faker,
) -> CreateProfileRequest:
    schema = choice([extracted_data_schema, document_layout_schema])

    return CreateProfileRequest(
        name=faker.name(),
        schema_=schema,
        format=choice(["json", "excel"]),
    )


@pytest.fixture
def create_profile_request_model_schema_and_with_external_storages(
    extracted_data_schema,
    document_layout_schema,
    profile_external_storages_info,
    faker,
) -> CreateProfileRequest:
    schema = choice([extracted_data_schema, document_layout_schema])

    return CreateProfileRequest(
        name=faker.name(),
        schema_=schema,
        format=choice(["json", "excel"]),
        external_storages_info=profile_external_storages_info,
    )


@pytest.fixture
def document_type_id():
    return uuid4().hex


@pytest.fixture
def document_type(document_type_id, test_tenant_id):
    return DocumentTypeFactory.create(document_type_id, test_tenant_id)


@pytest.fixture
def profile_schema(extracted_data_schema, document_layout_schema):
    return choice([extracted_data_schema, document_layout_schema])


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
        SerializedDocumentLayoutSchema: document_layout_schema_data,
        SerializedExtractedDataSchema: extracted_data_schema_data,
    }
    return class_to_fixture[type(profile_schema)]


@pytest.fixture
def build_output_request(document_type) -> BuildOutputRequest:
    return BuildOutputRequest(
        document_type_id=document_type.id(),
        profile_id=list(document_type.profiles.keys())[0],
    )


@pytest.fixture
def profile_info(document_type) -> ProfileInfo:
    profile = list(document_type.profiles.values())[0]
    return ProfileInfo(
        id_=profile.id,
        version=profile.version,
        schema_type=SchemaType.EXTRACTED_DATA,
    )


@pytest.fixture
def output_built(profile_info, test_tenant_id, faker) -> Output:
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info,
        document_id=str(faker.random_int()),
        state=OutputState.READY,
        file_path=faker.file_path(),
    )


@pytest.fixture
def profile_request_model_schema_and_with_external_storages(
    extracted_data_schema,
    document_layout_schema,
    profile_external_storages_info,
    faker,
) -> SaveProfileRequest:
    schema = choice([extracted_data_schema, document_layout_schema])

    return SaveProfileRequest(
        name=faker.name(),
        schema_=schema,
        external_storages_info=profile_external_storages_info,
    )
