from http import HTTPStatus

from deps_output_exporting.application import OutputService
from deps_output_exporting.constants import V1_API_PREFIX


class TestOutput:
    endpoint = V1_API_PREFIX

    def test_build_output__success(
        self, client, build_output_request, fake_document_type_repository, document_type, output_built, mocker
    ):
        fake_document_type_repository.save(document_type=document_type)
        mocker.patch.object(OutputService, "build_output", return_value=output_built)

        response = client.post(
            f"{self.endpoint}/document/{output_built.document_id}/outputs", data=build_output_request.model_dump_json()
        )

        assert response.status_code == HTTPStatus.CREATED

        res = response.json()
        profile = list(document_type.profiles.values())[0]
        assert res["tenantId"] == document_type.tenant_id()
        assert res["profileInfo"]["id"] == profile.id()
        assert res["profileInfo"]["version"] == profile.version
        assert res["documentId"] == output_built.document_id
        assert res["state"] == "ready"
        assert res["filePath"] == output_built.file_path
        assert res["creationDate"] == output_built.creation_date.isoformat()

    def test_build_output__document_type_not_found(self, client, build_output_request, fake_document_type_repository):
        response = client.post(f"{self.endpoint}/document/111/outputs", data=build_output_request.model_dump_json())

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_find_outputs__found__success(self, client, fake_output_repository, output):
        fake_output_repository.save(output=output)
        response = client.get(f"{self.endpoint}/document/{output.document_id}/outputs")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["outputs"]) == 1

        res_output = response.json()["outputs"][0]
        assert res_output["tenantId"] == output.tenant_id()
        assert res_output["profileInfo"]["id"] == output.profile_info.id()
        assert res_output["profileInfo"]["version"] == output.profile_info.version
        assert res_output["documentId"] == output.document_id
        assert res_output["state"] == output.state
        assert res_output["filePath"] == output.file_path
        assert res_output["creationDate"] == output.creation_date.isoformat()

    def test_find_outputs__no_outputs__success(self, client, fake_output_repository):
        response = client.get(f"{self.endpoint}/document/111/outputs")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["outputs"]) == 0

    def test_delete_output__deleted(self, client, fake_output_repository, output):
        fake_output_repository.save(output=output)
        client.delete(f"{self.endpoint}/document/{output.document_id}/outputs/{output.id.value}")
        response = client.get(f"{self.endpoint}/document/{output.document_id}/outputs")

        assert len(response.json()["outputs"]) == 0

    def test_delete_output__doesnt_exist__no_error(self, client, fake_output_repository):
        client.delete(f"{self.endpoint}/document/111/outputs/222")
