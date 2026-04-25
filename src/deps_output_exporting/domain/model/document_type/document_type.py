from typing import Optional

from ...exceptions import (
    AlreadyExistsError,
    BuiltinProfileEditingForbidden,
    ForbiddenError,
    PluginProfileEditingForbidden,
    ProfileNotFound,
)
from ..profile import ExternalStorageInfoData, Profile, SchemaData
from ..profile.builder import ProfileBuilder
from ..shared import EntityId, Guard, ImmutableCheck, TenantId

__all__ = ["DocumentType"]


class DocumentType:  # noqa: WPS338
    PROFILES_MIN_NUMBER = 1
    PROFILES_MAX_NUMBER = 10

    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())

    def __init__(self, tenant_id: TenantId, id_: EntityId, *, profiles: Optional[dict[str, Profile]] = None):
        self.id = id_
        self.tenant_id = tenant_id
        self.profiles = profiles if profiles is not None else {}

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def add_profile(
        self,
        name: str,
        schema: SchemaData,
        format_: str,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> EntityId:
        if self._is_profiles_limit(self.PROFILES_MAX_NUMBER):
            raise ForbiddenError(f"Number of profiles should not exceed {self.PROFILES_MAX_NUMBER}.")
        self._check_name_uniqueness(name)

        profile = (
            ProfileBuilder(name=name, format_=format_)
            .with_schema(schema_data=schema)
            .with_external_storages_info(external_storages_info=external_storages_info)
            .build()
        )
        self.profiles[profile.id()] = profile
        return profile.id

    def add_plugin_profile(
        self,
        profile_id: str,
        name: str,
        format_: str,
        schema_data: SchemaData | None,
    ) -> EntityId:
        profile = self.profiles.get(profile_id)
        if profile and not profile.is_updatable():
            raise BuiltinProfileEditingForbidden("Cannot update builtin profile.")
        builder = ProfileBuilder(name=name, format_=format_).with_id(profile_id).as_plugin()
        if schema_data:
            builder = builder.with_schema(schema_data)
        new_profile = builder.build()
        self.profiles[new_profile.id()] = new_profile
        return new_profile.id

    def update_profile(
        self,
        profile_id: str,
        name: str,
        schema: SchemaData,
        external_storages_info: Optional[list[ExternalStorageInfoData]] = None,
    ) -> EntityId:
        if (profile := self.profiles.get(profile_id)) is None:
            raise ProfileNotFound(profile_id)
        if profile.is_updatable():
            raise PluginProfileEditingForbidden("Cannot update plugin profile.")
        self._check_name_uniqueness(name, profile_id)
        profile.update(name=name, schema=schema, external_storages_info=external_storages_info)
        return profile.id

    def delete_profile(self, profile_id: str) -> None:
        if self.profiles.get(profile_id) is None:
            raise ProfileNotFound(profile_id)
        if self._is_profiles_limit(self.PROFILES_MIN_NUMBER):
            raise ForbiddenError("At least one profile should remain.")
        del self.profiles[profile_id]

    def _is_profiles_limit(self, limit: int) -> bool:
        return len(self.profiles) == limit

    def _check_name_uniqueness(self, name: str, profile_id: Optional[str] = None) -> None:
        names = [profile.name for profile in self.profiles.values() if profile.id() != profile_id]
        if name in names:
            raise AlreadyExistsError("Profile name must be unique.")

    def get_profile(self, profile_id: str) -> Profile:
        if (profile := self.profiles.get(profile_id)) is None:
            raise ProfileNotFound(profile_id)

        return profile
