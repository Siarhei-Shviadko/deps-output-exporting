from deps_output_exporting.domain.model import (
    Code,
    DocumentLayoutSchema,
    ExtractedDataSchema,
)
from deps_output_exporting.domain.model.profile.builder import ProfileBuilder


def test_update__profile_updated__version_changed(
    profile,
    profile_name,
    profile_schema_data,
):
    profile_id = profile.id
    creation_date = profile.creation_date
    version = profile.version

    profile.update(
        name=profile_name,
        schema=profile_schema_data,
    )

    assert profile.id == profile_id
    assert profile.creation_date == creation_date
    assert profile.version != version

    assert profile.name == profile_name

    if isinstance(profile_schema_data, ExtractedDataSchema):
        assert profile.schema.fields == profile_schema_data.fields
        assert profile.schema.needs_validation_results == profile_schema_data.needs_validation_results
    elif isinstance(profile_schema_data, DocumentLayoutSchema):
        assert profile.schema.parsing_type == profile_schema_data.parsing_type
        assert profile.schema.features == profile_schema_data.features


def test_create_with_schema__profile_created(profile_name, profile_schema_data, profile_format):
    profile = (
        ProfileBuilder(name=profile_name, format_=profile_format()).with_schema(schema_data=profile_schema_data).build()
    )

    assert profile.name == profile_name

    if isinstance(profile_schema_data, ExtractedDataSchema):
        assert profile.schema.fields == profile_schema_data.fields
        assert profile.schema.needs_validation_results == profile_schema_data.needs_validation_results
    elif isinstance(profile_schema_data, DocumentLayoutSchema):
        assert profile.schema.parsing_type == profile_schema_data.parsing_type
        assert profile.schema.features == profile_schema_data.features


def test_update__profile_updated__with_schema_and_external_storages__version_changed(
    profile,
    profile_name,
    profile_schema_data,
    external_storages_info_schema_data,
):
    profile_id = profile.id
    creation_date = profile.creation_date
    version = profile.version

    profile.update(
        name=profile_name,
        schema=profile_schema_data,
        external_storages_info=external_storages_info_schema_data,
    )

    assert profile.id == profile_id
    assert profile.creation_date == creation_date
    assert profile.version != version

    assert profile.name == profile_name

    if isinstance(profile_schema_data, ExtractedDataSchema):
        assert profile.schema.fields == profile_schema_data.fields
        assert profile.schema.needs_validation_results == profile_schema_data.needs_validation_results
    elif isinstance(profile_schema_data, DocumentLayoutSchema):
        assert profile.schema.parsing_type == profile_schema_data.parsing_type
        assert profile.schema.features == profile_schema_data.features

    for profile_external_storage_info, external_storage_info_schema_data in zip(
        profile.external_storages_info, external_storages_info_schema_data
    ):
        assert profile_external_storage_info.code == external_storage_info_schema_data["code"]
        assert (
            profile_external_storage_info.output_directory_path
            == external_storage_info_schema_data["output_directory_path"]
        )


def test_create_with_schema_and_external_storages__profile_created(
    profile_name,
    profile_schema_data,
    profile_format,
    external_storages_info_schema_data,
):
    profile = (
        ProfileBuilder(name=profile_name, format_=profile_format())
        .with_schema(schema_data=profile_schema_data)
        .with_external_storages_info(external_storages_info_schema_data)
        .build()
    )

    assert profile.name == profile_name

    if isinstance(profile_schema_data, ExtractedDataSchema):
        assert profile.schema.fields == profile_schema_data.fields
        assert profile.schema.needs_validation_results == profile_schema_data.needs_validation_results
    elif isinstance(profile_schema_data, DocumentLayoutSchema):
        assert profile.schema.parsing_type == profile_schema_data.parsing_type
        assert profile.schema.features == profile_schema_data.features

    for external_storage_info, expected_storage_info in zip(
        profile.external_storages_info, external_storages_info_schema_data
    ):
        assert external_storage_info.code == expected_storage_info["code"]

        assert external_storage_info.output_directory_path == expected_storage_info["output_directory_path"]
        if external_storage_info.code == Code.SALESFORCE:
            creds = external_storage_info.credentials
            expected_creds = expected_storage_info["credentials"]

            assert creds.client_id == expected_creds["client_id"]
            assert creds.client_secret == expected_creds["client_secret"]
            assert creds.owner_id == expected_creds["owner_id"]
            assert creds.location_id == expected_creds["location_id"]

        elif external_storage_info.code == Code.ONE_DRIVE:
            creds = external_storage_info.credentials
            expected_creds = expected_storage_info["credentials"]

            assert creds.client_id == expected_creds["client_id"]
            assert creds.secret == expected_creds["secret"]
            assert creds.tenant_id == expected_creds["tenant_id"]
            assert creds.user_id == expected_creds["user_id"]
