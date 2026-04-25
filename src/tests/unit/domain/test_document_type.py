from uuid import uuid4

import pytest

from deps_output_exporting.domain.exceptions import (
    AlreadyExistsError,
    ForbiddenError,
    PluginProfileEditingForbidden,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import (
    DocumentLayoutSchema,
    DocumentType,
    ExtractedDataSchema,
)


def test_add_profile__added(document_type, profile_name, profile_schema_data, profile_format):
    profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
    profile = document_type.profiles.get(profile_id.value)

    assert profile

    if isinstance(profile_schema_data, ExtractedDataSchema):
        assert profile.schema.fields == profile_schema_data.fields
        assert profile.schema.needs_validation_results == profile_schema_data.needs_validation_results
    elif isinstance(profile_schema_data, DocumentLayoutSchema):
        assert profile.schema.parsing_type == profile_schema_data.parsing_type
        assert profile.schema.features == profile_schema_data.features


def test_add_profile__number_exceeds__forbidden(document_type, profile_name, profile_schema_data, profile_format):
    for i in range(DocumentType.PROFILES_MAX_NUMBER - 1):
        document_type.add_profile(f"{profile_name}{i}", profile_schema_data, profile_format())

    with pytest.raises(ForbiddenError):
        document_type.add_profile("{profile_name}", profile_schema_data, profile_format())


def test_add_profile__name_exists__forbidden(document_type, profile_name, profile_schema_data, profile_format):
    document_type.add_profile(profile_name, profile_schema_data, profile_format())

    with pytest.raises(AlreadyExistsError):
        document_type.add_profile(profile_name, profile_schema_data, profile_format())


def test_update_profile__updated(document_type, profile_name, profile_schema_data, profile_format):
    profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
    document_type.update_profile(profile_id.value, "new_name", profile_schema_data)

    assert document_type.profiles[profile_id.value].name == "new_name"


def test_update_profile__profile_does_not_exist__raise_error(document_type, profile_id, profile_schema_data):
    with pytest.raises(ProfileNotFound):
        document_type.update_profile(profile_id, "new_name", profile_schema_data)


def test_update_profile__name_not_changed__no_error(
    document_type,
    profile_name,
    profile_schema_data,
    profile_format,
    new_extracted_data_schema_data,
    new_extracted_data_schema,
):
    profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
    document_type.update_profile(profile_id.value, profile_name, new_extracted_data_schema_data)

    assert document_type.profiles[profile_id.value].schema == new_extracted_data_schema


def test_update_profile__plugin_profile__raise_error(document_type, profile_name, profile_format, profile_schema_data):
    plugin_profile_id = uuid4().hex

    document_type.add_plugin_profile(
        profile_id=plugin_profile_id,
        name=profile_name,
        format_=profile_format(),
        schema_data=profile_schema_data,
    )

    with pytest.raises(PluginProfileEditingForbidden):
        document_type.update_profile(plugin_profile_id, "new_name", profile_schema_data)


def test_update_profile__name_changed__name_exists__forbidden(
    document_type, profile_name, profile_schema_data, profile_format
):
    profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
    document_type.add_profile("another profile", profile_schema_data, profile_format())

    with pytest.raises(AlreadyExistsError):
        document_type.update_profile(profile_id.value, "another profile", profile_schema_data)


def test_delete_profile__success(document_type, profile_name, profile_schema_data, profile_format):
    profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
    document_type.delete_profile(profile_id.value)

    assert len(document_type.profiles) == 1


def test_delete_profile__profile_does_not_exist__raise_error(document_type, profile_id):
    with pytest.raises(ProfileNotFound):
        document_type.delete_profile(profile_id)


def test_delete_the_only_profile__forbidden(document_type):
    profile_id = list(document_type.profiles.keys())[0]

    with pytest.raises(ForbiddenError):
        document_type.delete_profile(profile_id)
