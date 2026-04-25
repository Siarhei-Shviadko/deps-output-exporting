import copy

from deps_output_exporting.domain.model import DocumentType, ExportingType


class TestDocumentTypeRepository:
    def test_document_type_of_id__doc_type_exists__return_doc_type(self, document_type_repository, document_type):
        document_type_repository.save(document_type)
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert res == document_type

    def test_document_type_of_id__doc_type_does_not_exist__return_none(self, document_type_repository, document_type):
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert res == None

    def test_delete__doc_type_deleted(self, document_type_repository, document_type):
        document_type_repository.save(document_type)
        document_type_repository.delete(document_type.id(), document_type.tenant_id())
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert res == None

    def test_save__new_doc_type__saved(self, document_type_repository, document_type):
        document_type_repository.save(document_type)
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert res == document_type

    def test_save__existing_doc_type__updated(self, document_type_repository, document_type):
        document_type_repository.save(document_type)
        document_type.update_profile(
            profile_id=list(document_type.profiles.keys())[0],
            name="new name",
            schema={"fields": ["field1", "field2"], "needs_validation_results": False},
        )
        document_type_repository.save(document_type)
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert res == document_type

    def test_save__add_plugin__updated(self, document_type_repository, document_type: DocumentType, faker):
        document_type_repository.save(document_type)
        document_type.add_plugin_profile(
            profile_id=(profile_id := faker.uuid4()), name="New Profile", format_="pdf", schema_data=None
        )
        document_type_repository.save(document_type)
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
        assert (profile := res.profiles[profile_id])
        assert profile.name == "New Profile"
        assert profile.format() == "pdf"
        assert profile.exporting_type == ExportingType.PLUGIN

    def test_save__existing_profile_name__no_changes(
        self, document_type_repository, document_type, document_type__new_default_profile
    ):
        profile = list(document_type.profiles.values())[0]
        document_type_repository.save(document_type)
        document_type_repository.save(document_type__new_default_profile)
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert len(res.profiles) == 1

        res_profile = list(res.profiles.values())[0]

        assert res_profile.id() == profile.id()
        assert res_profile.name == profile.name
        assert res_profile.creation_date == profile.creation_date
        assert res_profile.schema == profile.schema
        assert res_profile.version == profile.version
        assert res_profile.format == profile.format

    def test_save_all__new_doc_type__saved(self, document_type_repository, document_type):
        document_type_repository.save_all([document_type])
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert res == document_type

    def test_save_all__existing_doc_type__not_changed(self, document_type_repository, document_type):
        same_doc_type = copy.deepcopy(document_type)

        document_type.update_profile(
            profile_id=list(document_type.profiles.keys())[0],
            name="new name",
            schema={"fields": ["field1", "field2"], "needs_validation_results": False},
        )
        profile = list(document_type.profiles.values())[0]
        document_type_repository.save(document_type)

        document_type_repository.save_all([same_doc_type])
        res = document_type_repository.document_type_of_id(same_doc_type.id(), same_doc_type.tenant_id())

        assert len(res.profiles) == 1

        res_profile = list(res.profiles.values())[0]

        assert res_profile.id() == profile.id()
        assert res_profile.name == profile.name
        assert res_profile.creation_date == profile.creation_date
        assert res_profile.schema == profile.schema
        assert res_profile.version == profile.version
        assert res_profile.format == profile.format

    def test_save_all__existing_profile_name__no_changes(
        self, document_type_repository, document_type, document_type__new_default_profile
    ):
        profile = list(document_type.profiles.values())[0]
        document_type_repository.save(document_type)
        document_type_repository.save_all([document_type__new_default_profile])
        res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

        assert len(res.profiles) == 1

        res_profile = list(res.profiles.values())[0]

        assert res_profile.id() == profile.id()
        assert res_profile.name == profile.name
        assert res_profile.creation_date == profile.creation_date
        assert res_profile.schema == profile.schema
        assert res_profile.version == profile.version
        assert res_profile.format == profile.format
