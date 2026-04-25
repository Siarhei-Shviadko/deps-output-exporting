from http import HTTPStatus

from deps_output_exporting.application import OutputServiceWithSagas
from deps_output_exporting.constants import V2_API_PREFIX


def test_build_output__success(
    fake_document_type_repository,
    client,
    build_output_request,
    document_type,
    output_built,
    mocker,
):
    fake_document_type_repository.save(document_type=document_type)
    mocker.patch.object(OutputServiceWithSagas, "build_outputs", return_value=None)

    response = client.post(
        f"{V2_API_PREFIX}/document/{output_built.document_id}/outputs", data=build_output_request.model_dump_json()
    )

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.text == ""


def test_build_output__document_type_not_found(client, build_output_request):
    response = client.post(f"{V2_API_PREFIX}/document/111/outputs", data=build_output_request.model_dump_json())

    assert response.status_code == HTTPStatus.NOT_FOUND
