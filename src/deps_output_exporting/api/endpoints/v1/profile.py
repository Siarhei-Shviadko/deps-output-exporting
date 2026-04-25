from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_output_exporting.api.auth import get_current_user_tenant
from deps_output_exporting.api.marker import MarkerRoute, Visibility
from deps_output_exporting.api.serializers import (
    AttachPluginRequest,
    AttachPluginResponse,
    CreateProfileRequest,
    ProfileResponse,
    ProfilesListResponse,
    SaveProfileRequest,
    SaveProfileResponse,
)
from deps_output_exporting.application import (
    DocumentTypeService,
    DocumentTypeServiceWithSagas,
)
from deps_output_exporting.containers import Containers

__all__ = ["profile_router"]

profile_router = APIRouter(route_class=MarkerRoute, tags=["Profile"])


@profile_router.post(
    "/document-types/{document_type_id}/profiles",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.CREATED,
    response_model=SaveProfileResponse,
)
@inject
def create_profile(
    document_type_id: str,
    profile_data: CreateProfileRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service_with_sagas]),
):
    if profile_data.external_storages_info is None:
        external_storages_info = None
    else:
        external_storages_info = [
            external_storage_info.model_dump(by_alias=False)
            for external_storage_info in profile_data.external_storages_info
        ]
    profile_id = application.create_profile(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        name=profile_data.name,
        schema=profile_data.schema_.model_dump(by_alias=False),
        format_=profile_data.format,
        external_storages_info=external_storages_info,
    )
    return SaveProfileResponse(id=profile_id())


@profile_router.put(
    "/document-types/{document_type_id}/profiles/{profile_id}",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.OK,
    response_model=SaveProfileResponse,
)
@inject
def update_profile(
    document_type_id: str,
    profile_id: str,
    profile_data: SaveProfileRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service]),
):
    if profile_data.external_storages_info is None:
        external_storages_info = None
    else:
        external_storages_info = [
            external_storage_info.model_dump(by_alias=False)
            for external_storage_info in profile_data.external_storages_info
        ]
    updated_profile_id = application.update_profile(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        profile_id=profile_id,
        name=profile_data.name,
        schema=profile_data.schema_.model_dump(by_alias=False),
        external_storages_info=external_storages_info,
    )
    return SaveProfileResponse(id=updated_profile_id())


@profile_router.delete(
    "/document-types/{document_type_id}/profiles/{profile_id}",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
)
@inject
def delete_profile(
    document_type_id: str,
    profile_id: str,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service_with_sagas]),
):
    application.delete_profile(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        profile_id=profile_id,
    )


@profile_router.get(
    "/document-types/{document_type_id}/profiles",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.OK,
    response_model=ProfilesListResponse,
)
@inject
def get_profiles(
    document_type_id: str,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service]),
):
    profiles = application.find_profiles(document_type_id, current_tenant)
    return ProfilesListResponse(profiles=[ProfileResponse.from_model(profile) for profile in profiles])


@profile_router.post(
    "/attach-plugin",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.OK,
    response_model=AttachPluginResponse,
)
@inject
def attach_plugin(
    plugin_data: AttachPluginRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeServiceWithSagas = Depends(Provide[Containers.document_type_service_with_sagas]),
):
    channel = application.attach_plugin(
        id_=plugin_data.id,
        tenant_id=current_tenant,
        name=plugin_data.name,
        format_=plugin_data.format,
        schema_data=(sc := plugin_data.schema) and sc.to_dto(),
    )
    return AttachPluginResponse(command_channel=channel)
