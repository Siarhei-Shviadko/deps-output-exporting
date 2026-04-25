from random import choice
from uuid import uuid4

import pytest

from deps_output_exporting.domain.model import (
    DocumentLayoutSchema,
    DocumentType,
    DocumentTypeFactory,
    EntityId,
    ExtractedDataSchema,
    Output,
    OutputState,
    ParsingFeature,
    ParsingType,
    ProfileInfo,
    SchemaData,
    SchemaType,
    TenantId,
)


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
def extracted_data_schema_data(extracted_data_schema) -> SchemaData:
    return SchemaData(
        fields=extracted_data_schema.fields, needs_validation_results=extracted_data_schema.needs_validation_results
    )


@pytest.fixture
def document_layout_schema() -> DocumentLayoutSchema:
    return DocumentLayoutSchema(parsing_type=ParsingType.TESSERACT, features=list(ParsingFeature))


@pytest.fixture
def document_layout_schema_data(document_layout_schema) -> SchemaData:
    return SchemaData(parsing_type=document_layout_schema.parsing_type, features=document_layout_schema.features)


@pytest.fixture
def profile_schema(extracted_data_schema, document_layout_schema):
    return choice([extracted_data_schema, document_layout_schema])


@pytest.fixture
def profile_schema_data(profile_schema, extracted_data_schema_data, document_layout_schema_data):
    class_to_fixture = {
        DocumentLayoutSchema: document_layout_schema_data,
        ExtractedDataSchema: extracted_data_schema_data,
    }
    return class_to_fixture[type(profile_schema)]


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
def new_output_of_profile(profile_info, test_tenant_id, faker, output_built) -> Output:
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info,
        document_id=output_built.document_id,
        state=OutputState.READY,
        file_path=faker.file_path(),
    )


@pytest.fixture
def doc_type_with_two_profiles(profile_extracted_data_schema, profile_document_layout_schema, test_tenant_id):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile_extracted_data_schema.id(): profile_extracted_data_schema,
            profile_document_layout_schema.id(): profile_document_layout_schema,
        },
    )


@pytest.fixture
def output_first_profile(doc_type_with_two_profiles, test_tenant_id, faker) -> Output:
    profile = list(doc_type_with_two_profiles.profiles.values())[0]
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=ProfileInfo(id_=profile.id, version=uuid4().hex, schema_type=SchemaType.EXTRACTED_DATA),
        document_id=str(faker.random_int()),
        state=OutputState.READY,
        file_path=faker.file_path(),
    )


@pytest.fixture
def output_second_profile(doc_type_with_two_profiles, output_first_profile, test_tenant_id, faker) -> Output:
    profile = list(doc_type_with_two_profiles.profiles.values())[1]
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=ProfileInfo(id_=profile.id, version=uuid4().hex, schema_type=SchemaType.DOCUMENT_LAYOUT),
        document_id=output_first_profile.document_id,
        state=OutputState.READY,
        file_path=faker.file_path(),
    )
