import pytest

from deps_output_exporting.domain.exceptions import (
    DocumentTypeNotFound,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import Output
from deps_output_exporting.infrastructure.services import OutputBuildingService


def test_build__output_built(
    fake_document_type_repository,
    fake_output_repository,
    output_service_with_sagas,
    document_type,
    output_built,
    test_tenant_id,
    mocker,
):
    fake_document_type_repository.save(document_type=document_type)
    mocker.patch.object(OutputBuildingService, "build", return_value=output_built)
    output = output_service_with_sagas.build_output_nosave(
        document_id=output_built.document_id,
        document_type_id=document_type.id(),
        tenant_id=test_tenant_id,
        profile_id=output_built.profile_info.id(),
    )
    assert isinstance(output, Output)
    assert output.document_id == output_built.document_id
    assert output.tenant_id() == test_tenant_id
    assert output.profile_info == output_built.profile_info


def test_build__document_type_not_found__raise_error(output_service_with_sagas, document_type, test_tenant_id):
    profile_id = list(document_type.profiles.keys())[0]
    with pytest.raises(DocumentTypeNotFound):
        output_service_with_sagas.build_output_nosave(
            document_id="111", document_type_id=document_type.id(), tenant_id=test_tenant_id, profile_id=profile_id
        )


def test_build__profile_not_found__raise_error(
    fake_document_type_repository, document_type, output_service_with_sagas, test_tenant_id
):
    fake_document_type_repository.save(document_type=document_type)
    with pytest.raises(ProfileNotFound):
        output_service_with_sagas.build_output_nosave(
            document_id="111",
            document_type_id=document_type.id(),
            tenant_id=test_tenant_id,
            profile_id="non_existing_profile_id",
        )
