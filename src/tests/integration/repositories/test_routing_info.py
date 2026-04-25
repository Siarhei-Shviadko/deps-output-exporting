class TestRoutingInfoRepository:
    def test_save__success(
        self,
        document_type_repository,
        routing_info_repository,
        document_type,
        routing_info,
    ):
        document_type_repository.save(document_type)
        routing_info_repository.save(routing_info)
        found_routing_info = routing_info_repository.find(
            routing_info.tenant_id(),
            routing_info.document_type_id(),
            routing_info.profile_id(),
        )

        assert found_routing_info == routing_info

    def test_find__routing_info(
        self,
        document_type_repository,
        routing_info_repository,
        document_type,
        routing_info,
    ):
        document_type_repository.save(document_type)
        routing_info_repository.save(routing_info)
        found_routing_info = routing_info_repository.find(
            routing_info.tenant_id(),
            routing_info.document_type_id(),
            routing_info.profile_id(),
        )
        assert found_routing_info == routing_info

    def test_find__no_routing_info(self, routing_info_repository, routing_info):
        found_routing_info = routing_info_repository.find(
            routing_info.tenant_id(),
            routing_info.document_type_id(),
            routing_info.profile_id(),
        )
        assert found_routing_info is None

    def test_delete__deleted(
        self,
        document_type_repository,
        routing_info_repository,
        document_type,
        routing_info,
    ):
        document_type_repository.save(document_type)
        routing_info_repository.save(routing_info)
        deleted_routing_info = routing_info_repository.delete(
            routing_info.tenant_id(),
            routing_info.document_type_id(),
            routing_info.profile_id(),
        )
        found_routing_info = routing_info_repository.find(
            routing_info.tenant_id(),
            routing_info.document_type_id(),
            routing_info.profile_id(),
        )

        assert deleted_routing_info == routing_info
        assert found_routing_info is None

    def test_delete__does_not_exist__no_error(self, routing_info_repository, routing_info):
        deleted_routing_info = routing_info_repository.delete(
            routing_info.tenant_id(),
            routing_info.document_type_id(),
            routing_info.profile_id(),
        )

        assert deleted_routing_info is None
