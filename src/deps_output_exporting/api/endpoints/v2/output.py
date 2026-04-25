from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response

from deps_output_exporting.api.auth import get_current_user_tenant
from deps_output_exporting.api.marker import MarkerRoute, Visibility
from deps_output_exporting.api.serializers import BuildOutputRequest, SerializedOutput
from deps_output_exporting.application import OutputServiceWithSagas
from deps_output_exporting.containers import Containers

__all__ = ["output_router"]

output_router = APIRouter(route_class=MarkerRoute, tags=["Output"])


@output_router.post(
    "/document/{documentId}/outputs",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.CREATED,
    response_model=SerializedOutput,
)
@inject
def build_outputs(
    output_data: BuildOutputRequest,
    document_id: str = Path(..., alias="documentId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: OutputServiceWithSagas = Depends(Provide[Containers.output_service_with_sagas]),
):
    application.build_outputs(
        document_id=document_id,
        document_type_id=output_data.document_type_id,
        tenant_id=current_tenant,
        profile_ids=[output_data.profile_id],
    )
    return Response(status_code=HTTPStatus.ACCEPTED)
