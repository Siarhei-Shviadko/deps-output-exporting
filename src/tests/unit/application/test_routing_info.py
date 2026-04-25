import pytest

from deps_output_exporting.application import RoutingInfoService
from deps_output_exporting.domain.exceptions import (
    DocumentTypeNotFound,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import (
    IDocumentTypeRepository,
    IRoutingInfoRepository,
    RoutingInfo,
)


class TestRoutingInfoService:
    def test_create_routing_info_doc_type_and_profile_exist__created(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        fake_routing_info_repository: IRoutingInfoRepository,
        routing_info_service: RoutingInfoService,
        doc_type_with_two_profiles,
        profile_extracted_data_schema,
    ):
        fake_document_type_repository.save(document_type=doc_type_with_two_profiles)
        profile_id = profile_extracted_data_schema.id()
        document_type_id = doc_type_with_two_profiles.id()
        tenant_id = doc_type_with_two_profiles.tenant_id()

        created_routing_info = routing_info_service.create_routing_info(
            tenant_id=tenant_id, document_type_id=document_type_id, profile_id=profile_id, command_channel="test"
        )

        assert isinstance(created_routing_info, RoutingInfo)
        assert created_routing_info.document_type_id() == document_type_id
        assert created_routing_info.tenant_id() == tenant_id
        assert created_routing_info.profile_id() == profile_id

    def test_create_profile_doc_type_not_exists__raises(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        routing_info_service: RoutingInfoService,
        document_type_id,
        test_tenant_id,
        profile_id,
    ):
        with pytest.raises(DocumentTypeNotFound):
            routing_info_service.create_routing_info(
                tenant_id=test_tenant_id,
                document_type_id=document_type_id,
                profile_id=profile_id,
                command_channel="test",
            )

    def test_create_profile_doc_type_exists_profiles_not_exist__raises(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        routing_info_service: RoutingInfoService,
        document_type,
        profile_id,
    ):
        fake_document_type_repository.save(document_type=document_type)
        with pytest.raises(ProfileNotFound):
            routing_info_service.create_routing_info(
                tenant_id=document_type.tenant_id(),
                document_type_id=document_type.id(),
                profile_id=profile_id,
                command_channel="test",
            )

    def test_delete_routing_info__deleted(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        fake_routing_info_repository: IRoutingInfoRepository,
        routing_info_service: RoutingInfoService,
        doc_type_with_two_profiles,
        profile_extracted_data_schema,
    ):
        fake_document_type_repository.save(document_type=doc_type_with_two_profiles)
        profile_id = profile_extracted_data_schema.id()
        document_type_id = doc_type_with_two_profiles.id()
        tenant_id = doc_type_with_two_profiles.tenant_id()

        routing_info_service.delete_routing_info(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            profile_id=profile_id,
        )
        removed_routing_info = fake_routing_info_repository.find(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            profile_id=profile_id,
        )

        assert removed_routing_info is None
