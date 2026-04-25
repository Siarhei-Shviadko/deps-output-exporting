from deps_output_exporting.domain.model import (
    DocumentLayoutSchema,
    ExternalStorageInfoFactory,
    ExtractedDataSchema,
)
from deps_output_exporting.domain.model.profile.builder import ProfileBuilder


def test_create_profile__with_builder__with_schema(profile_name, profile_schema_data, profile_format):
    built_profile = (
        ProfileBuilder(name=profile_name, format_=profile_format()).with_schema(schema_data=profile_schema_data).build()
    )

    assert built_profile.name == profile_name
    assert built_profile.format == profile_format

    if isinstance(profile_schema_data, ExtractedDataSchema):
        assert built_profile.schema.fields == profile_schema_data.fields
        assert built_profile.schema.needs_validation_results == profile_schema_data.needs_validation_results
    elif isinstance(profile_schema_data, DocumentLayoutSchema):
        assert built_profile.schema.parsing_type == profile_schema_data.parsing_type
        assert built_profile.schema.features == profile_schema_data.features


def test_create_profile__with_builder__with_schema_and_external_storages_info(
    profile_name,
    profile_schema_data,
    external_storages_info_schema_data,
    profile_format,
):
    built_profile = (
        ProfileBuilder(
            name=profile_name,
            format_=profile_format(),
        )
        .with_schema(schema_data=profile_schema_data)
        .with_external_storages_info(
            external_storages_info=external_storages_info_schema_data,
        )
        .build()
    )

    assert built_profile.name == profile_name
    assert built_profile.format == profile_format

    built_external_storages_info = built_profile.external_storages_info
    expected_external_storages_info = ExternalStorageInfoFactory.create_external_storages_info(
        external_storages_info_schema_data,
    )

    for built_external_storage_info, expected_external_storage_info in zip(
        built_external_storages_info, expected_external_storages_info
    ):
        assert built_external_storage_info.code.value == expected_external_storage_info.code.value
        assert built_external_storage_info.output_directory_path == expected_external_storage_info.output_directory_path
