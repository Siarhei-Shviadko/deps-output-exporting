import json

from cryptography.fernet import Fernet

from deps_output_exporting.constants import CRYPT_CREDENTIALS_KEY
from deps_output_exporting.infrastructure.repositories import DocumentTypeMapper


def test_document_type_mapper___without_external_storages_info__to_dict(doc_type_two_types_of_profile):
    profile1 = list(doc_type_two_types_of_profile.profiles.values())[0]
    profile2 = list(doc_type_two_types_of_profile.profiles.values())[1]
    expected_result = {
        "id": doc_type_two_types_of_profile.id(),
        "tenant_id": doc_type_two_types_of_profile.tenant_id(),
        "profiles": [
            {
                "id": profile1.id(),
                "name": profile1.name,
                "creation_date": profile1.creation_date,
                "schema": {
                    "fields": profile1.schema.fields,
                    "needs_validation_results": profile1.schema.needs_validation_results,
                },
                "version": profile1.version,
                "format": profile1.format.value,
                "document_type_id": doc_type_two_types_of_profile.id(),
                "external_storages_info": None,
                "exporting_type": profile1.exporting_type,
            },
            {
                "id": profile2.id(),
                "name": profile2.name,
                "creation_date": profile2.creation_date,
                "schema": {
                    "parsing_type": profile2.schema.parsing_type.value,
                    "features": [feature.value for feature in profile2.schema.features],
                },
                "version": profile2.version,
                "format": profile2.format.value,
                "document_type_id": doc_type_two_types_of_profile.id(),
                "external_storages_info": None,
                "exporting_type": profile2.exporting_type,
            },
        ],
    }

    result = DocumentTypeMapper.to_dict(doc_type_two_types_of_profile)
    assert result["id"] == expected_result["id"]
    assert result["tenant_id"] == expected_result["tenant_id"]
    assert result["profiles"] == expected_result["profiles"]


def test_document_type_mapper__without_external_storages_info__from_row(
    doc_type_two_types_of_profile, test_document_type_row
):
    profile1 = list(doc_type_two_types_of_profile.profiles.values())[0]
    profile2 = list(doc_type_two_types_of_profile.profiles.values())[1]
    document_type_row = test_document_type_row(
        id=doc_type_two_types_of_profile.id(),
        tenant_id=doc_type_two_types_of_profile.tenant_id(),
        profiles=[
            {
                "id": profile1.id(),
                "name": profile1.name,
                "creation_date": str(profile1.creation_date),
                "schema": {
                    "fields": profile1.schema.fields,
                    "needs_validation_results": profile1.schema.needs_validation_results,
                },
                "version": profile1.version,
                "format": profile1.format,
                "exporting_type": profile1.exporting_type,
                "document_type_id": doc_type_two_types_of_profile.id(),
            },
            {
                "id": profile2.id(),
                "name": profile2.name,
                "creation_date": str(profile2.creation_date),
                "schema": {
                    "parsing_type": profile2.schema.parsing_type.value,
                    "features": [feature.value for feature in profile2.schema.features],
                },
                "version": profile2.version,
                "format": profile2.format,
                "exporting_type": profile2.exporting_type,
                "document_type_id": doc_type_two_types_of_profile.id(),
            },
        ],
    )

    result = DocumentTypeMapper.from_row(document_type_row)
    assert result == doc_type_two_types_of_profile


def test_document_type_mapper___with_external_storages_info__to_dict(
    doc_type_two_types_of_profile_with_external_storages_info,
):
    profile1 = list(doc_type_two_types_of_profile_with_external_storages_info.profiles.values())[0]
    profile2 = list(doc_type_two_types_of_profile_with_external_storages_info.profiles.values())[1]
    external_storages_info1 = profile1.external_storages_info[0]
    external_storages_info2 = profile2.external_storages_info[0]

    expected_result = {
        "id": doc_type_two_types_of_profile_with_external_storages_info.id(),
        "tenant_id": doc_type_two_types_of_profile_with_external_storages_info.tenant_id(),
        "profiles": [
            {
                "id": profile1.id(),
                "name": profile1.name,
                "creation_date": profile1.creation_date,
                "schema": {
                    "fields": profile1.schema.fields,
                    "needs_validation_results": profile1.schema.needs_validation_results,
                },
                "version": profile1.version,
                "format": profile1.format.value,
                "exporting_type": profile1.exporting_type,
                "document_type_id": doc_type_two_types_of_profile_with_external_storages_info.id(),
                "external_storages_info": [
                    {
                        "code": external_storages_info1.code.value,
                        "credentials": external_storages_info1.credentials,
                        "output_directory_path": external_storages_info1.output_directory_path,
                    },
                ],
            },
            {
                "id": profile2.id(),
                "name": profile2.name,
                "creation_date": profile2.creation_date,
                "schema": {
                    "parsing_type": profile2.schema.parsing_type.value,
                    "features": [feature.value for feature in profile2.schema.features],
                },
                "version": profile2.version,
                "format": profile2.format.value,
                "exporting_type": profile2.exporting_type,
                "document_type_id": doc_type_two_types_of_profile_with_external_storages_info.id(),
                "external_storages_info": [
                    {
                        "code": external_storages_info2.code.value,
                        "credentials": external_storages_info2.credentials,
                        "output_directory_path": external_storages_info2.output_directory_path,
                    },
                ],
            },
        ],
    }

    result = DocumentTypeMapper.to_dict(doc_type_two_types_of_profile_with_external_storages_info)
    assert result["id"] == expected_result["id"]
    assert result["tenant_id"] == expected_result["tenant_id"]

    result_external_storages1 = result["profiles"][0].pop("external_storages_info")[0]
    expected_external_storages1 = expected_result["profiles"][0].pop("external_storages_info")[0]

    result_external_storages2 = result["profiles"][1].pop("external_storages_info")[0]
    expected_external_storages2 = expected_result["profiles"][1].pop("external_storages_info")[0]

    assert result["profiles"] == expected_result["profiles"]

    assert result_external_storages1["code"] == expected_external_storages1["code"]
    assert result_external_storages1["output_directory_path"] == expected_external_storages1["output_directory_path"]

    assert result_external_storages2["code"] == expected_external_storages2["code"]
    assert result_external_storages2["output_directory_path"] == expected_external_storages2["output_directory_path"]


def test_document_type_mapper__with_external_storages_info__from_row(
    doc_type_two_types_of_profile_with_external_storages_info,
    test_document_type_row,
):
    profile1 = list(doc_type_two_types_of_profile_with_external_storages_info.profiles.values())[0]
    profile2 = list(doc_type_two_types_of_profile_with_external_storages_info.profiles.values())[1]
    external_storages_info1 = profile1.external_storages_info[0]
    external_storages_info2 = profile2.external_storages_info[0]
    fernet_key = Fernet(CRYPT_CREDENTIALS_KEY.encode())
    document_type_row = test_document_type_row(
        id=doc_type_two_types_of_profile_with_external_storages_info.id(),
        tenant_id=doc_type_two_types_of_profile_with_external_storages_info.tenant_id(),
        profiles=[
            {
                "id": profile1.id(),
                "name": profile1.name,
                "creation_date": str(profile1.creation_date),
                "schema": {
                    "fields": profile1.schema.fields,
                    "needs_validation_results": profile1.schema.needs_validation_results,
                },
                "version": profile1.version,
                "format": profile1.format,
                "exporting_type": profile1.exporting_type,
                "document_type_id": doc_type_two_types_of_profile_with_external_storages_info.id(),
                "external_storages_info": [
                    {
                        "code": external_storages_info1.code.value,
                        "credentials": fernet_key.encrypt(
                            json.dumps(
                                {
                                    "client_id": external_storages_info1.credentials.client_id,
                                    "client_secret": external_storages_info1.credentials.client_secret,
                                    "owner_id": external_storages_info1.credentials.owner_id,
                                    "location_id": external_storages_info1.credentials.location_id,
                                }
                            ).encode()
                        ).decode(),
                        "output_directory_path": external_storages_info1.output_directory_path,
                    },
                ],
            },
            {
                "id": profile2.id(),
                "name": profile2.name,
                "creation_date": str(profile2.creation_date),
                "schema": {
                    "parsing_type": profile2.schema.parsing_type.value,
                    "features": [feature.value for feature in profile2.schema.features],
                },
                "version": profile2.version,
                "format": profile2.format,
                "exporting_type": profile2.exporting_type,
                "document_type_id": doc_type_two_types_of_profile_with_external_storages_info.id(),
                "external_storages_info": [
                    {
                        "code": external_storages_info2.code.value,
                        "credentials": fernet_key.encrypt(
                            json.dumps(
                                {
                                    "client_id": external_storages_info2.credentials.client_id,
                                    "secret": external_storages_info2.credentials.secret,
                                    "tenant_id": external_storages_info2.credentials.tenant_id,
                                    "user_id": external_storages_info2.credentials.user_id,
                                }
                            ).encode()
                        ).decode(),
                        "output_directory_path": external_storages_info2.output_directory_path,
                    },
                ],
            },
        ],
    )

    result = DocumentTypeMapper.from_row(document_type_row)
    assert result == doc_type_two_types_of_profile_with_external_storages_info
