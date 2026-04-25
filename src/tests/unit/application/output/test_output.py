import pytest

from deps_output_exporting.application import OutputService
from deps_output_exporting.domain.exceptions import (
    DocumentTypeNotFound,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import Output
from deps_output_exporting.infrastructure.services import OutputBuildingService


class TestOutputService:
    def test_build__output_built(
        self,
        fake_document_type_repository,
        fake_output_repository,
        output_service,
        document_type,
        output_built,
        test_tenant_id,
        mocker,
    ):
        fake_document_type_repository.save(document_type=document_type)
        mocker.patch.object(OutputBuildingService, "build", return_value=output_built)
        output = output_service.build_output(
            document_id=output_built.document_id,
            document_type_id=document_type.id(),
            tenant_id=test_tenant_id,
            profile_id=output_built.profile_info.id(),
        )

        assert fake_output_repository._output_db[output.id()] == output
        assert isinstance(output, Output)

    def test_build__document_type_not_found__raise_error(self, output_service, document_type, test_tenant_id):
        profile_id = list(document_type.profiles.keys())[0]
        with pytest.raises(DocumentTypeNotFound):
            output_service.build_output(
                document_id="111", document_type_id=document_type.id(), tenant_id=test_tenant_id, profile_id=profile_id
            )

    def test_build__profile_not_found__raise_error(
        self, fake_document_type_repository, document_type, output_service, test_tenant_id
    ):
        fake_document_type_repository.save(document_type=document_type)
        with pytest.raises(ProfileNotFound):
            output_service.build_output(
                document_id="111",
                document_type_id=document_type.id(),
                tenant_id=test_tenant_id,
                profile_id="non_existing_profile_id",
            )

    def test_build__old_outputs_of_profile_deleted(
        self,
        fake_document_type_repository,
        fake_output_repository,
        output_service,
        document_type,
        output_built,
        test_tenant_id,
        mocker,
        new_output_of_profile,
    ):
        fake_document_type_repository.save(document_type=document_type)
        mocker.patch.object(OutputBuildingService, "build", return_value=output_built)
        output = output_service.build_output(
            document_id=output_built.document_id,
            document_type_id=document_type.id(),
            tenant_id=test_tenant_id,
            profile_id=output_built.profile_info.id(),
        )

        mocker.patch.object(OutputBuildingService, "build", return_value=new_output_of_profile)
        new_output = output_service.build_output(
            document_id=new_output_of_profile.document_id,
            document_type_id=document_type.id(),
            tenant_id=test_tenant_id,
            profile_id=new_output_of_profile.profile_info.id(),
        )

        outputs = output_service.find_outputs_by_document_id(output.document_id, output.tenant_id())

        assert len(outputs) == 1
        assert outputs[0] == new_output

    def test_build__outputs_of_another_profile_not_deleted(
        self,
        fake_document_type_repository,
        fake_output_repository,
        output_service,
        test_tenant_id,
        mocker,
        doc_type_with_two_profiles,
        output_first_profile,
        output_second_profile,
    ):
        fake_document_type_repository.save(document_type=doc_type_with_two_profiles)
        mocker.patch.object(OutputBuildingService, "build", return_value=output_first_profile)
        first_output = output_service.build_output(
            document_id=output_first_profile.document_id,
            document_type_id=doc_type_with_two_profiles.id(),
            tenant_id=test_tenant_id,
            profile_id=output_first_profile.profile_info.id(),
        )

        mocker.patch.object(OutputBuildingService, "build", return_value=output_second_profile)
        second__output = output_service.build_output(
            document_id=output_second_profile.document_id,
            document_type_id=doc_type_with_two_profiles.id(),
            tenant_id=test_tenant_id,
            profile_id=output_second_profile.profile_info.id(),
        )

        outputs = output_service.find_outputs_by_document_id(first_output.document_id, first_output.tenant_id())

        assert len(outputs) == 2
        assert outputs == [first_output, second__output]

    def test_find_by_document_id__found__success(self, fake_output_repository, output, output_service):
        fake_output_repository.save(output=output)
        outputs = output_service.find_outputs_by_document_id(output.document_id, output.tenant_id())

        assert len(outputs) == 1
        assert outputs[0] == output

    def test_find_by_document_id__no_outputs__success(self, output, output_service):
        outputs = output_service.find_outputs_by_document_id(output.document_id, output.tenant_id())

        assert len(outputs) == 0

    def test_delete_output__deleted__event_sent(self, fake_output_repository, output, output_service, mocker):
        fake_output_repository.save(output=output)
        sent_event = mocker.patch.object(OutputService, "_send_event")
        output_service.delete_output(output.document_id, output.tenant_id(), output.id())
        document_outputs = fake_output_repository.find_by_document_id(output.tenant_id(), output.document_id)

        assert len(document_outputs) == 0
        sent_event.assert_called_with(output.document_id, output.file_path)

    def test_delete_document_edata_outputs__edata_output_deleted__event_sent(
        self, fake_output_repository, output_edata_schema, output_service, mocker
    ):
        fake_output_repository.save(output=output_edata_schema)
        sent_event = mocker.patch.object(OutputService, "_send_event")
        output_service.delete_document_edata_outputs(output_edata_schema.document_id, output_edata_schema.tenant_id())
        document_outputs = fake_output_repository.find_by_document_id(
            output_edata_schema.tenant_id(), output_edata_schema.document_id
        )

        assert len(document_outputs) == 0
        sent_event.assert_called_with(output_edata_schema.document_id, output_edata_schema.file_path)

    def test_delete_document_edata_outputs__document_layout_output_not_deleted(
        self, fake_output_repository, output_dl_schema, output_service
    ):
        fake_output_repository.save(output=output_dl_schema)
        output_service.delete_document_edata_outputs(output_dl_schema.document_id, output_dl_schema.tenant_id())
        document_outputs = fake_output_repository.find_by_document_id(
            output_dl_schema.tenant_id(), output_dl_schema.document_id
        )

        assert len(document_outputs) == 1
