from typing import Any

from sqlalchemy import Row

from deps_output_exporting.domain.model import (
    EntityId,
    Output,
    OutputState,
    ProfileInfo,
    SchemaType,
    TenantId,
)

__all__ = ["OutputMapper"]


class ProfileInfoMapper:
    @staticmethod
    def from_dict(raw_profile_info: dict[str, Any]) -> ProfileInfo:
        return ProfileInfo(
            id_=EntityId(raw_profile_info["id"]),
            version=raw_profile_info["version"],
            schema_type=raw_profile_info["schema_type"] and SchemaType(raw_profile_info["schema_type"]),
        )

    @staticmethod
    def to_dict(profile_info: ProfileInfo) -> dict[str, Any]:
        return {
            "id": profile_info.id(),
            "version": profile_info.version,
            "schema_type": profile_info.schema_type and profile_info.schema_type.value,
        }


class OutputMapper:
    @staticmethod
    def from_row(raw_output: Row) -> Output:
        return Output(
            id_=EntityId(raw_output.id),
            tenant_id=TenantId(raw_output.tenant_id),
            profile_info=ProfileInfoMapper.from_dict(raw_output.profile_info),
            document_id=raw_output.document_id,
            state=OutputState(raw_output.state),
            file_path=raw_output.file_path,
            creation_date=raw_output.creation_date,
        )

    @staticmethod
    def to_dict(output: Output) -> dict[str, Any]:
        return {
            "id": output.id(),
            "tenant_id": output.tenant_id(),
            "profile_info": ProfileInfoMapper.to_dict(output.profile_info),
            "document_id": output.document_id,
            "state": output.state.value,
            "file_path": output.file_path,
            "creation_date": output.creation_date,
        }
