class TestOutputRepository:
    def test_save_find_by_document_id__success(self, output_repository, output):
        output_repository.save(output)
        res = output_repository.find_by_document_id(output.tenant_id(), output.document_id)

        assert len(res) == 1
        assert res[0] == output

    def test_save__updated_state__saved(self, output_repository, output, output_updated_state):
        output_repository.save(output)
        output_repository.save(output_updated_state)
        res = output_repository.find_by_document_id(output.tenant_id(), output.document_id)

        assert len(res) == 1
        assert res[0] == output_updated_state

    def test_find_by_document_id__no_outputs(self, output_repository, output):
        assert output_repository.find_by_document_id(output.tenant_id(), output.document_id) == []

    def test_delete__deleted(self, output_repository, output):
        output_repository.save(output)
        delete_res = output_repository.delete(output.tenant_id(), output.document_id, output.id())
        find_res = output_repository.find_by_document_id(output.tenant_id(), output.document_id)

        assert delete_res == output
        assert find_res == []

    def test_delete__does_not_exist__no_error(self, output_repository, output):
        output_repository.delete(output.tenant_id(), output.document_id, output.id())

    def test_delete_all__one_output__deleted(self, output_repository, output):
        output_repository.save(output)
        output_repository.delete_all(output.tenant_id(), [output.id()])

        assert output_repository.find_by_document_id(output.tenant_id(), output.document_id) == []

    def test_delete_all__two_outputs__deleted(self, output_repository, output, output2):
        output_repository.save(output)
        output_repository.save(output2)
        output_repository.delete_all(output.tenant_id(), [output.id(), output2.id()])

        assert output_repository.find_by_document_id(output.tenant_id(), output.document_id) == []

    def test_delete_all__no_outputs__no_error(self, output_repository, output):
        output_repository.delete_all(output.tenant_id(), [output.id()])

    def test_delete_outdated_outputs__deleted(self, output_repository, output, new_output_of_profile):
        output_repository.save(output)
        output_repository.save(new_output_of_profile)

        deleted_outputs = output_repository.delete_outdated_outputs(
            output.document_id,
            output.tenant_id(),
            output.profile_info.id(),
        )

        assert deleted_outputs[0] == output
        assert output_repository.find_by_document_id(output.tenant_id(), output.document_id) == [new_output_of_profile]

    def test_delete_outdated_outputs__output_of_another_profile_not_deleted(
        self, output_repository, output, new_output_another_profile
    ):
        output_repository.save(output)
        output_repository.save(new_output_another_profile)

        deleted_outputs = output_repository.delete_outdated_outputs(
            output.document_id,
            output.tenant_id(),
            output.profile_info.id(),
        )

        assert deleted_outputs == []
        assert output_repository.find_by_document_id(output.tenant_id(), output.document_id) == [
            output,
            new_output_another_profile,
        ]
