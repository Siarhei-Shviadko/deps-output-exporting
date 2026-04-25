from http import HTTPStatus

from fastapi import status

from deps_output_exporting.constants import V1_API_PREFIX
from deps_output_exporting.domain.model import (
    Code,
    DocumentLayoutSchema,
    ExtractedDataSchema,
    IDocumentTypeRepository,
)


class TestProfile:
    endpoint = V1_API_PREFIX

    def test_create_profile_with_schema_success(
        self,
        client,
        create_profile_request_model_with_schema,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type,
    ):
        fake_document_type_repository.save(document_type=document_type)
        response = client.post(
            f"{self.endpoint}/document-types/{document_type.id()}/profiles",
            data=create_profile_request_model_with_schema.model_dump_json(),
        )
        assert response.status_code == status.HTTP_201_CREATED
        profile_id = response.json()["id"]
        assert response.json() == {"id": profile_id}
        document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type.id(), tenant_id=document_type.tenant_id()
        )
        profile = document_type.profiles[profile_id]
        assert profile.name == create_profile_request_model_with_schema.name
        assert profile.format() == create_profile_request_model_with_schema.format
        if isinstance(profile.schema, ExtractedDataSchema):
            assert profile.schema.fields == create_profile_request_model_with_schema.schema_.fields
            assert (
                profile.schema.needs_validation_results
                == create_profile_request_model_with_schema.schema_.needs_validation_results
            )
        elif isinstance(profile.schema, DocumentLayoutSchema):
            assert profile.schema.parsing_type == create_profile_request_model_with_schema.schema_.parsing_type
            assert profile.schema.features == create_profile_request_model_with_schema.schema_.features
        else:
            assert False, "Unexpected schema type"

    def test_create_profile_document_type_not_found(
        self,
        client,
        fake_document_type_repository: IDocumentTypeRepository,
        create_profile_request_model_with_schema,
    ):
        not_existed_document_type_id = "not_existed_document_type_id"
        response = client.post(
            f"{self.endpoint}/document-types/{not_existed_document_type_id}/profiles",
            data=create_profile_request_model_with_schema.model_dump_json(),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_profile__success(
        self,
        client,
        profile_request_model,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type,
        profile_name,
        profile_schema_data,
        profile_format,
    ):
        profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
        fake_document_type_repository.save(document_type=document_type)
        response = client.put(
            f"{self.endpoint}/document-types/{document_type.id.value}/profiles/{profile_id.value}",
            data=profile_request_model.model_dump_json(),
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": profile_id.value}

    def test_update_profile__document_type_not_found__error(
        self,
        client,
        profile_request_model,
        document_type_id,
        profile_id,
        fake_document_type_repository: IDocumentTypeRepository,
    ):
        response = client.put(
            f"{self.endpoint}/document-types/{document_type_id}/profiles/{profile_id}",
            data=profile_request_model.model_dump_json(),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_profile__deleted(
        self,
        document_type,
        profile_name,
        profile_schema_data,
        profile_format,
        fake_document_type_repository: IDocumentTypeRepository,
        client,
    ):
        profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
        fake_document_type_repository.save(document_type=document_type)
        response = client.delete(
            f"{self.endpoint}/document-types/{document_type.id.value}/profiles/{profile_id.value}",
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert len(document_type.profiles) == 1

    def test_delete_profile__document_type_not_found__error(
        self,
        client,
        document_type_id,
        profile_id,
        fake_document_type_repository: IDocumentTypeRepository,
    ):
        response = client.delete(
            f"{self.endpoint}/document-types/{document_type_id}/profiles/{profile_id}",
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_profiles__success(self, client, document_type, fake_document_type_repository):
        fake_document_type_repository.save(document_type=document_type)

        response = client.get(
            f"{self.endpoint}/document-types/{document_type.id.value}/profiles",
        )

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["profiles"]) == 1

    def test_get_profiles__document_type_not_found__error(
        self, client, document_type_id, fake_document_type_repository
    ):
        response = client.get(
            f"{self.endpoint}/document-types/{document_type_id}/profiles",
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_profiles__correct_response(
        self,
        client,
        doc_type_two_types_of_profile,
        fake_document_type_repository,
        profile_extracted_data_schema,
        profile_document_layout_schema,
    ):
        fake_document_type_repository.save(document_type=doc_type_two_types_of_profile)

        response = client.get(
            f"{self.endpoint}/document-types/{doc_type_two_types_of_profile.id.value}/profiles",
        )

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["profiles"]) == 2

        response_profile1 = response.json()["profiles"][0]
        response_profile2 = response.json()["profiles"][1]

        assert response_profile1["id"] == profile_extracted_data_schema.id()
        assert response_profile1["name"] == profile_extracted_data_schema.name
        assert response_profile1["creationDate"] == str(profile_extracted_data_schema.creation_date.date())
        assert response_profile1["schema"]["fields"] == profile_extracted_data_schema.schema.fields
        assert (
            response_profile1["schema"]["needsValidationResults"]
            == profile_extracted_data_schema.schema.needs_validation_results
        )
        assert response_profile1["version"] == profile_extracted_data_schema.version

        assert response_profile2["id"] == profile_document_layout_schema.id()
        assert response_profile2["name"] == profile_document_layout_schema.name
        assert response_profile2["creationDate"] == str(profile_document_layout_schema.creation_date.date())
        assert response_profile2["schema"]["features"] == profile_document_layout_schema.schema.features
        assert response_profile2["version"] == profile_document_layout_schema.version

    def test_create_profile_with_schema_and_external_storages_info_success(
        self,
        client,
        create_profile_request_model_schema_and_with_external_storages,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type,
    ):
        create_profile_request_model = create_profile_request_model_schema_and_with_external_storages
        fake_document_type_repository.save(document_type=document_type)
        response = client.post(
            f"{self.endpoint}/document-types/{document_type.id()}/profiles",
            data=create_profile_request_model.model_dump_json(),
        )
        assert response.status_code == status.HTTP_201_CREATED
        profile_id = response.json()["id"]
        assert response.json() == {"id": profile_id}
        document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type.id(), tenant_id=document_type.tenant_id()
        )
        profile = document_type.profiles[profile_id]
        assert profile.name == create_profile_request_model.name
        assert profile.format() == create_profile_request_model.format

        for external_storage_info, create_request_expected_storage_info in zip(
            profile.external_storages_info, create_profile_request_model.external_storages_info
        ):
            assert external_storage_info.code == create_request_expected_storage_info.code
            assert (
                external_storage_info.output_directory_path
                == create_request_expected_storage_info.output_directory_path
            )
            if external_storage_info.code == Code.SALESFORCE:
                creds = external_storage_info.credentials
                expected_creds = create_request_expected_storage_info.credentials

                assert creds.client_id == expected_creds.client_id
                assert creds.client_secret == expected_creds.client_secret
                assert creds.owner_id == expected_creds.owner_id
                assert creds.location_id == expected_creds.location_id

            elif external_storage_info.code == Code.ONE_DRIVE:
                creds = external_storage_info.credentials
                expected_creds = create_request_expected_storage_info.credentials

                assert creds.client_id == expected_creds.client_id
                assert creds.secret == expected_creds.secret
                assert creds.tenant_id == expected_creds.tenant_id
                assert creds.user_id == expected_creds.user_id

    def test_update_profile__with_schema_and_external_storages_info__success(
        self,
        client,
        profile_request_model_schema_and_with_external_storages,
        fake_document_type_repository,
        document_type,
        profile_name,
        profile_schema_data,
        profile_format,
    ):
        profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
        fake_document_type_repository.save(document_type=document_type)
        response = client.put(
            f"{self.endpoint}/document-types/{document_type.id.value}/profiles/{profile_id.value}",
            data=profile_request_model_schema_and_with_external_storages.model_dump_json(),
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": profile_id.value}

    def test_get_profiles__with_schema_and_external_storages_info__correct_response(
        self,
        client,
        doc_type_two_types_of_profile_with_external_storages_info,
        fake_document_type_repository,
        profile_extracted_data_schema_with_external_storages_info,
        profile_document_layout_schema_with_external_storages_info,
    ):
        profile_extracted_data = profile_extracted_data_schema_with_external_storages_info
        profile_document_layout = profile_document_layout_schema_with_external_storages_info
        fake_document_type_repository.save(document_type=doc_type_two_types_of_profile_with_external_storages_info)

        response = client.get(
            f"{self.endpoint}/document-types/{doc_type_two_types_of_profile_with_external_storages_info.id.value}/profiles",
        )

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["profiles"]) == 2

        response_profile1 = response.json()["profiles"][0]
        response_profile2 = response.json()["profiles"][1]

        assert response_profile1["id"] == profile_extracted_data.id()
        assert response_profile1["name"] == profile_extracted_data.name
        assert response_profile1["creationDate"] == str(profile_extracted_data.creation_date.date())
        assert response_profile1["schema"]["fields"] == profile_extracted_data.schema.fields
        assert (
            response_profile1["schema"]["needsValidationResults"]
            == profile_extracted_data.schema.needs_validation_results
        )
        assert response_profile1["version"] == profile_extracted_data.version

        assert response_profile2["id"] == profile_document_layout.id()
        assert response_profile2["name"] == profile_document_layout.name
        assert response_profile2["creationDate"] == str(profile_document_layout.creation_date.date())
        assert response_profile2["schema"]["features"] == profile_document_layout.schema.features
        assert response_profile2["version"] == profile_document_layout.version

        for external_storage_info, expected_storage_info in zip(
            response_profile1["externalStoragesInfo"], profile_extracted_data.external_storages_info
        ):
            assert external_storage_info["code"] == expected_storage_info.code

        for external_storage_info, expected_storage_info in zip(
            response_profile2["externalStoragesInfo"], profile_document_layout.external_storages_info
        ):
            assert external_storage_info["code"] == expected_storage_info.code
