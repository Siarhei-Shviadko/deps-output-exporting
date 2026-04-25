from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_output_exporting.api.auth import get_current_user_tenant
from deps_output_exporting.api.marker import MarkerRoute, Visibility
from deps_output_exporting.api.serializers import (
    BuildOutputRequest,
    OutputsListResponse,
    SerializedOutput,
)
from deps_output_exporting.application import OutputService
from deps_output_exporting.containers import Containers

__all__ = ["output_router"]

output_router = APIRouter(route_class=MarkerRoute, tags=["Output"])


@output_router.post(
    "/document/{document_id}/outputs",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.CREATED,
    response_model=SerializedOutput,
)
@inject
def build_output(
    document_id: str,
    output_data: BuildOutputRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    application: OutputService = Depends(Provide[Containers.output_service]),
):
    output = application.build_output(
        document_id=document_id,
        tenant_id=current_tenant,
        document_type_id=output_data.document_type_id,
        profile_id=output_data.profile_id,
    )
    return SerializedOutput.from_model(output)


@output_router.get(
    "/document/{document_id}/outputs",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.OK,
    response_model=OutputsListResponse,
)
@inject
def find_outputs(
    document_id: str,
    current_tenant: str = Depends(get_current_user_tenant),
    application: OutputService = Depends(Provide[Containers.output_service]),
):
    outputs = application.find_outputs_by_document_id(
        document_id=document_id,
        tenant_id=current_tenant,
    )
    return OutputsListResponse(outputs=[SerializedOutput.from_model(output) for output in outputs])


@output_router.delete(
    "/document/{document_id}/outputs/{output_id}",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
)
@inject
def delete_output(
    document_id: str,
    output_id: str,
    current_tenant: str = Depends(get_current_user_tenant),
    application: OutputService = Depends(Provide[Containers.output_service]),
):
    application.delete_output(
        document_id=document_id,
        output_id=output_id,
        tenant_id=current_tenant,
    )
