import copy
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from faker import Faker
from openpyxl.workbook import Workbook

from deps_output_exporting.constants import DEFAULT_PROFILE_NAME
from deps_output_exporting.domain.model import (
    Code,
    DocumentLayoutSchema,
    DocumentType,
    EntityId,
    ExportingType,
    ExternalStorageInfo,
    ExtractedDataSchema,
    Format,
    ParsingFeature,
    ParsingType,
    Profile,
    TenantId,
)
from deps_output_exporting.infrastructure.proxies import FileStorageProxy, KeyValue
from deps_output_exporting.infrastructure.services import (
    ExcelDataBuilder,
    GeneralInfo,
    OutputBuildingService,
)
from tests.data import (
    document_detail_dict,
    document_layout_dict,
    document_layout_kvp_feature_dict,
    document_layout_merged_tables,
    document_type_dict,
    extracted_data_dict,
    key_values_dict,
    unified_data_dict,
    validation_result_dict,
)

from .fields_data_fixtures import (
    fields_data__all_fields_with_validation,
    fields_data__some_fields_all_valid,
    fields_data__some_fields_without_validation,
    fields_data__table_field,
)

fake = Faker()


@pytest.fixture
def profile__edata_json_all_fields(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=[
                "checkbox_1",
                "checkbox_list_1",
                "enum_1",
                "enum_list_1",
                "kv_pair_1",
                "kv_pair_list_1",
                "string_1",
                "string_list_1",
                "table_1",
                "table_list_1",
                "checkbox_2",
                "checkbox_list_2",
                "enum_2",
                "enum_list_2",
                "kv_pair_2",
                "kv_pair_list_2",
                "string_2",
                "string_list_2",
                "table_2",
                "table_list_2",
            ],
            needs_validation_results=True,
        ),
        format_=Format("json"),
        version=uuid4().hex,
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def profile__edata_json_some_fields(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["checkbox_1", "enum_1", "kv_pair_1", "string_1", "table_1"],
            needs_validation_results=True,
        ),
        format_=Format("json"),
        version=uuid4().hex,
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def document_type__edata_json_all_fields_profile(profile__edata_json_all_fields, test_tenant_id):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile__edata_json_all_fields.id(): profile__edata_json_all_fields,
        },
    )


@pytest.fixture
def document_type__edata_json_some_fields_profile(profile__edata_json_some_fields, test_tenant_id):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile__edata_json_some_fields.id(): profile__edata_json_some_fields,
        },
    )


@pytest.fixture
def get_extracted_data_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-extraction:8000/api/extraction/v2/extracted-data/{document_id}",
        status_code=200,
        json=extracted_data_dict,
    )
    yield requests_mock


@pytest.fixture
def get_document_type_success_request_mock(
    requests_mock,
    document_type__edata_json_all_fields_profile,
    document_type__edata_json_some_fields_profile,
    document_type__edata_excel_profiles,
    document_type__profiles_with_external_storages,
    document_type__no_fields_profiles,
    document_type__dl_excel_profiles,
):
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__edata_json_all_fields_profile.id.value}",
        status_code=200,
        json=document_type_dict,
    )
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__edata_json_some_fields_profile.id.value}",
        status_code=200,
        json=document_type_dict,
    )
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__edata_excel_profiles.id.value}",
        status_code=200,
        json=document_type_dict,
    )
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__profiles_with_external_storages.id.value}",
        status_code=200,
        json=document_type_dict,
    )
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__no_fields_profiles.id.value}",
        status_code=200,
        json=document_type_dict,
    )
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__dl_excel_profiles.id.value}",
        status_code=200,
        json=document_type_dict,
    )
    yield requests_mock


@pytest.fixture
def get_document_type_success_request_mock__no_engine(
    requests_mock,
    document_type__edata_excel_profiles,
    document_type__dl_excel_profiles,
):
    doc_type_dict_no_engine = copy.deepcopy(document_type_dict)
    doc_type_dict_no_engine["engine"] = None
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__edata_excel_profiles.id.value}",
        status_code=200,
        json=doc_type_dict_no_engine,
    )
    requests_mock.register_uri(
        "GET",
        f"http://deps-document-type:8000/api/document-type/v1/types/{document_type__dl_excel_profiles.id.value}",
        status_code=200,
        json=doc_type_dict_no_engine,
    )
    yield requests_mock


@pytest.fixture
def get_document_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-document-api:8000/api/document/v1/documents/{document_id}",
        status_code=200,
        json=document_detail_dict,
    )
    yield requests_mock


@pytest.fixture
def get_document_success_request_mock__no_engine(requests_mock, document_id):
    doc_detail_dict_no_engine = copy.deepcopy(document_detail_dict)
    doc_detail_dict_no_engine["engine"] = None
    requests_mock.get(
        f"http://deps-document-api:8000/api/document/v1/documents/{document_id}",
        status_code=200,
        json=doc_detail_dict_no_engine,
    )
    yield requests_mock


@pytest.fixture
def get_unifier_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-unifier:8000/api/unifier/v1/unified_data/{document_id}",
        status_code=200,
        json=unified_data_dict,
    )
    yield requests_mock


@pytest.fixture
def get_validation_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-validation-api:8000/api/validation/v1/results/{document_id}",
        status_code=200,
        json=validation_result_dict,
    )
    yield requests_mock


@pytest.fixture
def get_validation_success_request_mock__all_valid(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-validation-api:8000/api/validation/v1/results/{document_id}",
        status_code=200,
        json={"isValid": True, "detail": []},
    )
    yield requests_mock


@pytest.fixture
def get_validation_not_found_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-validation-api:8000/api/validation/v1/results/{document_id}",
        status_code=404,
    )
    yield requests_mock


@pytest.fixture
def profile__edata_excel_all_fields_with_validation(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=[
                "checkbox_1",
                "checkbox_list_1",
                "enum_1",
                "enum_list_1",
                "kv_pair_1",
                "kv_pair_list_1",
                "string_1",
                "string_list_1",
                "table_1",
                "table_list_1",
                "checkbox_2",
                "checkbox_list_2",
                "enum_2",
                "enum_list_2",
                "kv_pair_2",
                "kv_pair_list_2",
                "string_2",
                "string_list_2",
                "table_2",
                "table_list_2",
            ],
            needs_validation_results=True,
        ),
        format_=Format("excel"),
        version=uuid4().hex,
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def profile__edata_excel_some_fields_with_validation(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["checkbox_1", "enum_1", "kv_pair_1", "string_1", "table_1"],
            needs_validation_results=True,
        ),
        format_=Format("excel"),
        version=uuid4().hex,
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def profile__edata_excel_some_fields_without_validation(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["checkbox_1", "enum_1", "kv_pair_1", "string_1", "table_1"],
            needs_validation_results=False,
        ),
        format_=Format("excel"),
        version=uuid4().hex,
        exporting_type=ExportingType.BUILT_IN,
    )


@pytest.fixture
def document_type__edata_excel_profiles(
    profile__edata_excel_all_fields_with_validation,
    profile__edata_excel_some_fields_with_validation,
    profile__edata_excel_some_fields_without_validation,
    test_tenant_id,
):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile__edata_excel_all_fields_with_validation.id(): profile__edata_excel_all_fields_with_validation,
            profile__edata_excel_some_fields_with_validation.id(): profile__edata_excel_some_fields_with_validation,
            profile__edata_excel_some_fields_without_validation.id(): profile__edata_excel_some_fields_without_validation,
        },
    )


@pytest.fixture
def general_info():
    return GeneralInfo(
        title="Document Title",
        type="AllFieldTypesQA",
        uploaded_date=datetime.fromisoformat("2023-12-11T11:52:02.004368-05:00"),
        fields_number=18,
        engine="TESSERACT",
    )


@pytest.fixture
def general_info__no_fields_profile():
    return GeneralInfo(
        title="Document Title",
        type="AllFieldTypesQA",
        uploaded_date=datetime.fromisoformat("2023-12-11T11:52:02.004368-05:00"),
        fields_number=0,
        engine="TESSERACT",
    )


@pytest.fixture
def general_info__some_fields_with_validation_results():
    return GeneralInfo(
        title="Document Title",
        type="AllFieldTypesQA",
        uploaded_date=datetime.fromisoformat("2023-12-11T11:52:02.004368-05:00"),
        fields_number=5,
        engine="TESSERACT",
    )


@pytest.fixture
def excel_data_builder(general_info, fields_data__all_fields_with_validation):
    return ExcelDataBuilder(
        general_info=general_info,
        fields_data=fields_data__all_fields_with_validation,
    )


@pytest.fixture
def test_workbook():
    workbook = Workbook()
    active = workbook.active
    workbook.remove(active)
    return workbook


@pytest.fixture()
def generated_name_json():
    return f"{uuid4().hex}.json"


@pytest.fixture()
def mocked_file_storage_request(mocker, generated_name_json):
    mock = mocker.patch.object(FileStorageProxy, "upload_file", return_value=f"output/{generated_name_json}")
    return mock


@pytest.fixture()
def mocked_output_service_file_name_generator(mocker, generated_name_json):
    mock = mocker.patch.object(
        OutputBuildingService,
        "_generate_file_name",
        return_value=generated_name_json,
    )
    return mock


@pytest.fixture
def profile__salesforce_info(faker, profile_salesforce_credentials):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["checkbox_1", "enum_1", "kv_pair_1", "string_1", "table_1"],
            needs_validation_results=True,
        ),
        format_=Format("json"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
        external_storages_info=[
            ExternalStorageInfo(
                code=Code.SALESFORCE,
                credentials=profile_salesforce_credentials,
                output_directory_path=fake.uri_path(),
            ),
        ],
    )


@pytest.fixture
def profile__onedrive_info(faker, profile_one_drive_credentials):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["checkbox_1", "enum_1", "kv_pair_1", "string_1", "table_1"],
            needs_validation_results=True,
        ),
        format_=Format("json"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
        external_storages_info=[
            ExternalStorageInfo(
                code=Code.ONE_DRIVE,
                credentials=profile_one_drive_credentials,
                output_directory_path=fake.uri_path(),
            ),
        ],
    )


@pytest.fixture
def profile__salesforce_onedrive_info(faker, profile_one_drive_credentials, profile_salesforce_credentials):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=["checkbox_1", "enum_1", "kv_pair_1", "string_1", "table_1"],
            needs_validation_results=True,
        ),
        format_=Format("json"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
        external_storages_info=[
            ExternalStorageInfo(
                code=Code.SALESFORCE,
                credentials=profile_salesforce_credentials,
                output_directory_path=fake.uri_path(),
            ),
            ExternalStorageInfo(
                code=Code.ONE_DRIVE,
                credentials=profile_one_drive_credentials,
                output_directory_path=fake.uri_path(),
            ),
        ],
    )


@pytest.fixture
def document_type__profiles_with_external_storages(
    profile__salesforce_info, profile__onedrive_info, profile__salesforce_onedrive_info, test_tenant_id
):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile__salesforce_info.id(): profile__salesforce_info,
            profile__onedrive_info.id(): profile__onedrive_info,
            profile__salesforce_onedrive_info.id(): profile__salesforce_onedrive_info,
        },
    )


@pytest.fixture
def external_storage_info__onedrive(profile_one_drive_credentials):
    return ExternalStorageInfo(
        code=Code.ONE_DRIVE,
        credentials=profile_one_drive_credentials,
        output_directory_path=fake.uri_path(),
    )


@pytest.fixture
def put_onedrive_success_request_mock(requests_mock, external_storage_info__onedrive, generated_name_json):
    credentials = external_storage_info__onedrive.credentials
    path = external_storage_info__onedrive.output_directory_path
    requests_mock.put(
        f"https://graph.microsoft.com/v1.0/users/{credentials.user_id}/drive/root:/{path}/{generated_name_json}:/content",
        status_code=201,
    )
    yield requests_mock


@pytest.fixture
def put_onedrive_error_request_mock(requests_mock, external_storage_info__onedrive, generated_name_json):
    credentials = external_storage_info__onedrive.credentials
    path = external_storage_info__onedrive.output_directory_path
    requests_mock.put(
        f"https://graph.microsoft.com/v1.0/users/{credentials.user_id}/drive/root:/{path}/{generated_name_json}:/content",
        status_code=400,
        json={"error": {"code": "error_code", "message": "Error message"}},
    )
    yield requests_mock


@pytest.fixture
def salesforce_access_token():
    return uuid4().hex


@pytest.fixture
def external_storage_info__salesforce(profile_salesforce_credentials):
    return ExternalStorageInfo(
        code=Code.SALESFORCE,
        credentials=profile_salesforce_credentials,
        output_directory_path=None,
    )


@pytest.fixture
def salesforse_auth_success_request_mock(requests_mock, salesforce_access_token):
    requests_mock.post(
        "https://my-domain-name.my.salesforce.com/services/oauth2/token",
        status_code=200,
        json={"access_token": salesforce_access_token},
    )
    yield requests_mock


@pytest.fixture
def salesforse_auth_error_request_mock(requests_mock):
    requests_mock.post(
        "https://my-domain-name.my.salesforce.com/services/oauth2/token",
        status_code=400,
        json={"error": "invalid_client_id", "error_description": "client identifier invalid"},
    )
    yield requests_mock


@pytest.fixture
def salesforse_upload_success_request_mock(requests_mock):
    requests_mock.post(
        "https://my-domain-name.my.salesforce.com/services/data/v60.0/sobjects/ContentVersion",
        status_code=201,
    )
    yield requests_mock


@pytest.fixture
def salesforse_upload_error_request_mock(requests_mock):
    requests_mock.post(
        "https://my-domain-name.my.salesforce.com/services/data/v60.0/sobjects/ContentVersion",
        status_code=400,
        json=[
            {
                "message": "Required fields are missing: [Title]",
                "errorCode": "REQUIRED_FIELD_MISSING",
                "fields": ["Title"],
            },
            {"message": "The argument is null or invalid.", "errorCode": "INVALID_ARGUMENT_TYPE", "fields": []},
        ],
    )
    yield requests_mock


@pytest.fixture
def file_name_json():
    return uuid4().hex + ".json"


@pytest.fixture
def file_name_excel():
    return uuid4().hex + ".xlsx"


@pytest.fixture
def upload_json_file_mock(mocker, file_name_json):
    return mocker.patch.object(FileStorageProxy, "upload_file", return_value=f"output/{file_name_json}")


@pytest.fixture
def upload_excel_file_mock(mocker, file_name_excel):
    return mocker.patch.object(FileStorageProxy, "upload_file", return_value=f"output/{file_name_excel}")


@pytest.fixture
def profile__dl_json_all_features(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=DocumentLayoutSchema(
            parsing_type=ParsingType.TESSERACT,
            features=list(ParsingFeature),
        ),
        format_=Format("json"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
    )


@pytest.fixture
def profile__dl_json_one_feature(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=DocumentLayoutSchema(
            parsing_type=ParsingType.TESSERACT,
            features=[ParsingFeature.KEY_VALUE_PAIRS],
        ),
        format_=Format("json"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
    )


@pytest.fixture
def profile__dl_excel_all_features(faker):
    return Profile(
        id_=EntityId(),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=DocumentLayoutSchema(
            parsing_type=ParsingType.TESSERACT,
            features=list(ParsingFeature),
        ),
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
    )


@pytest.fixture
def document_type__dl_json_profiles(profile__dl_json_all_features, profile__dl_json_one_feature, test_tenant_id):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile__dl_json_all_features.id(): profile__dl_json_all_features,
            profile__dl_json_one_feature.id(): profile__dl_json_one_feature,
        },
    )


@pytest.fixture
def document_type__dl_excel_profiles(profile__dl_excel_all_features, test_tenant_id):
    return DocumentType(
        id_=EntityId(),
        tenant_id=TenantId(test_tenant_id),
        profiles={profile__dl_excel_all_features.id(): profile__dl_excel_all_features},
    )


@pytest.fixture
def get_document_layout_all_features_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-parsing:8000/api/parsing/v1/document-layout/{document_id}",
        status_code=200,
        json=document_layout_dict,
    )
    yield requests_mock


@pytest.fixture
def get_document_layout_with_merged_tables_all_features_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-parsing:8000/api/parsing/v1/document-layout/{document_id}",
        status_code=200,
        json=document_layout_merged_tables,
    )
    yield requests_mock


@pytest.fixture
def get_document_layout_kvp_feature_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-parsing:8000/api/parsing/v1/document-layout/{document_id}",
        status_code=200,
        json=document_layout_kvp_feature_dict,
    )
    yield requests_mock


@pytest.fixture
def get_prompter_key_values_success_request_mock(requests_mock, document_id):
    requests_mock.get(
        f"http://deps-prompter:8000/api/prompter/v1/documents/{document_id}/key-values",
        status_code=200,
        json=key_values_dict,
    )
    yield requests_mock


@pytest.fixture
def profile__edata_json_no_fields(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=[],
            needs_validation_results=True,
        ),
        format_=Format("json"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
    )


@pytest.fixture
def profile__edata_excel_no_fields(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=faker.name(),
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=[],
            needs_validation_results=True,
        ),
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
    )


@pytest.fixture
def profile__edata_excel_default_no_fields(faker):
    return Profile(
        id_=EntityId(uuid4().hex),
        name=DEFAULT_PROFILE_NAME,
        creation_date=datetime.now(timezone.utc),
        schema=ExtractedDataSchema(
            fields=[],
            needs_validation_results=True,
        ),
        format_=Format("excel"),
        exporting_type=ExportingType.BUILT_IN,
        version=uuid4().hex,
    )


@pytest.fixture
def document_type__no_fields_profiles(profile__edata_json_no_fields, profile__edata_excel_no_fields, test_tenant_id):
    return DocumentType(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profiles={
            profile__edata_json_no_fields.id(): profile__edata_json_no_fields,
            profile__edata_excel_no_fields.id(): profile__edata_excel_no_fields,
        },
    )


@pytest.fixture
def key_values() -> list[KeyValue]:
    key_values = []
    for kv in key_values_dict["key_values"]:
        key_values.append(KeyValue(key=kv["key"], value=kv["value"]))

    return key_values
