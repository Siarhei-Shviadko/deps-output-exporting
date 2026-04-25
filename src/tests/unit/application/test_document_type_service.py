from datetime import datetime
from typing import Optional
from uuid import uuid4

import pytest

from deps_output_exporting.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_output_exporting.domain.exceptions import (
    DocumentTypeNotFound,
    PluginProfileEditingForbidden,
    ProfileNotFound,
)
from deps_output_exporting.domain.model import (
    DocumentType,
    DocumentTypeData,
    DocumentTypeFactory,
    EntityId,
    ExtractedDataSchema,
    GetDocumentTypes,
    IDocumentTypeRepository,
    Profile,
    Schema,
)
from tests.fakes import FakeCommandProducer


class TestDocumentTypeService:
    def compare_profiles(
        self,
        p1: Profile,
        p2: Optional[Profile] = None,
        *,
        p2_id: Optional[EntityId] = None,
        p2_name: Optional[str] = None,
        p2_creation_date: Optional[datetime] = None,
        p2_schema: Optional[Schema] = None,
    ):
        if p2:
            p2_id = p2.id
            p2_name = p2.name
            p2_creation_date = p2.creation_date
            p2_schema = p2.schema
        assert p1.id == p2_id
        assert p1.name == p2_name
        assert p1.creation_date == p2_creation_date
        assert p1.schema == p2_schema

    def compare_document_types(self, dt1: DocumentType, dt2: DocumentType):
        assert dt1.id == dt2.id
        assert dt1.tenant_id == dt2.tenant_id
        assert dt1.profiles.keys() == dt2.profiles.keys()
        for key in dt1.profiles:
            self.compare_profiles(p1=dt1.profiles[key], p2=dt2.profiles[key])

    def test_initialize_document_type__command_sent(
        self, document_type_service, fake_command_producer: FakeCommandProducer
    ):
        fake_command_producer.reset_commands()
        document_type_service.initialize()
        assert fake_command_producer.channel_reply_commands[COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL] == [
            GetDocumentTypes()
        ]

    def test_find_document_type__not_found__raise_error(self, document_type_service, document_type):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.find_document_type(document_type.id(), document_type.tenant_id())

    def test_find_document_type__found(self, fake_document_type_repository, document_type_service, document_type):
        fake_document_type_repository.save(document_type)
        found_doc_type = document_type_service.find_document_type(document_type.id(), document_type.tenant_id())
        self.compare_document_types(document_type, found_doc_type)

    def test_save__saved__default_profile_created(
        self, fake_document_type_repository, document_type_service, document_type_id, test_tenant_id
    ):
        document_type_service.save_document_type(document_type_id=document_type_id, tenant_id=test_tenant_id)
        saved_doc_type = fake_document_type_repository.document_type_of_id(document_type_id, test_tenant_id)
        assert saved_doc_type
        assert len(saved_doc_type.profiles) == 1

        profile = list(saved_doc_type.profiles.values())[0]
        assert profile.name == "Default Profile"
        assert isinstance(profile.schema, ExtractedDataSchema)

    def test_delete__doc_type_exist__deleted(self, fake_document_type_repository, document_type_service, document_type):
        fake_document_type_repository.save(document_type)
        assert fake_document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
        document_type_service.delete_document_type(document_type.id(), document_type.tenant_id())
        assert not fake_document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    def test_delete__doc_type_doesnt_exist__deleted(
        self, fake_document_type_repository, document_type_service, document_type
    ):
        assert document_type_service.delete_document_type(document_type.id(), document_type.tenant_id()) is None

    def test_create_profile_doc_type_exist__created(
        self,
        profile_name,
        profile_schema,
        profile_schema_data,
        profile_format,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service,
        document_type,
    ):
        fake_document_type_repository.save(document_type=document_type)
        profile_id = document_type_service.create_profile(
            document_type_id=document_type.id(),
            tenant_id=document_type.tenant_id(),
            name=profile_name,
            schema=profile_schema_data,
            format_=profile_format(),
        )
        updated_doc_type = fake_document_type_repository.document_type_of_id(
            document_type.id(), document_type.tenant_id()
        )
        assert len(updated_doc_type.profiles.keys()) == 2
        created_profile = updated_doc_type.profiles[profile_id()]
        assert created_profile.id == profile_id
        assert created_profile.name == profile_name
        assert created_profile.schema == profile_schema

    def test_create_profile_doc_type_not_exists_raises(
        self,
        profile_name,
        profile_schema_data,
        profile_format,
        fake_document_type_repository,
        document_type_service,
        test_tenant_id,
        document_type_id,
    ):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.create_profile(
                document_type_id=document_type_id,
                tenant_id=test_tenant_id,
                name=profile_name,
                schema=profile_schema_data,
                format_=profile_format(),
            )

    def test_save_document_types_doc_types_not_exist__saved(
        self, test_tenant_id, document_type_service, fake_document_type_repository
    ):
        document_types_data = [
            DocumentTypeData(document_type_id=uuid4().hex, tenant_id=test_tenant_id) for _ in range(5)
        ]
        document_type_service.save_document_types(document_types_data)
        for doc_type in document_types_data:
            saved_doc_type = fake_document_type_repository.document_type_of_id(
                doc_type["document_type_id"], doc_type["tenant_id"]
            )
            created_doc_type = DocumentTypeFactory.create(
                id_=doc_type["document_type_id"], tenant_id=doc_type["tenant_id"]
            )
            assert created_doc_type.id == saved_doc_type.id
            assert created_doc_type.tenant_id == saved_doc_type.tenant_id

    def test_save_document_types__some_doc_types_exist__existing_doc_types_are_not_overriden(
        self,
        document_type_service,
        fake_document_type_repository,
        profile_name,
        profile_schema_data,
        profile_format,
        document_type,
    ):
        document_type.add_profile(name=profile_name, schema=profile_schema_data, format_=profile_format())
        fake_document_type_repository.save(document_type)
        same_doc_type_without_profiles_data = DocumentTypeData(
            document_type_id=document_type.id(), tenant_id=document_type.tenant_id()
        )
        document_type_service.save_document_types([same_doc_type_without_profiles_data])
        doc_type_from_storage = fake_document_type_repository.document_type_of_id(
            document_type.id(), document_type.tenant_id()
        )
        self.compare_document_types(doc_type_from_storage, document_type)

    def test_update_profile__updated(
        self,
        document_type_service,
        fake_document_type_repository,
        document_type,
        profile_name,
        profile_schema_data,
        profile_format,
    ):
        profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
        fake_document_type_repository.save(document_type=document_type)
        updated_profile_id = document_type_service.update_profile(
            document_type_id=document_type.id(),
            tenant_id=document_type.tenant_id(),
            profile_id=profile_id(),
            name="new_name",
            schema=profile_schema_data,
        )

        assert updated_profile_id == profile_id
        assert document_type.profiles[profile_id.value].name == "new_name"

    def test_update_profile__doc_type_does_not_exist__raise_error(
        self, document_type_service, document_type_id, test_tenant_id, profile_schema_data, profile_id
    ):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.update_profile(
                document_type_id=document_type_id,
                tenant_id=test_tenant_id,
                profile_id=profile_id,
                name="new_name",
                schema=profile_schema_data,
            )

    def test_update_profile__profile_does_not_exist__raise_error(
        self,
        document_type_service,
        fake_document_type_repository,
        document_type,
        test_tenant_id,
        profile_id,
        profile_schema_data,
    ):
        fake_document_type_repository.save(document_type=document_type)

        with pytest.raises(ProfileNotFound):
            document_type_service.update_profile(
                document_type_id=document_type.id(),
                tenant_id=test_tenant_id,
                profile_id=profile_id,
                name="new_name",
                schema=profile_schema_data,
            )

    def test_update_profile__plugin_profile__raise_error(
        self,
        document_type_service,
        fake_document_type_repository,
        document_type,
        profile_name,
        profile_format,
        profile_schema_data,
    ):
        plugin_profile_id = uuid4().hex
        document_type.add_plugin_profile(
            profile_id=plugin_profile_id, name=profile_name, format_=profile_format(), schema_data=profile_schema_data
        )

        fake_document_type_repository.save(document_type=document_type)

        with pytest.raises(PluginProfileEditingForbidden):
            document_type_service.update_profile(
                document_type_id=document_type.id(),
                tenant_id=document_type.tenant_id(),
                profile_id=plugin_profile_id,
                name="new_name",
                schema=profile_schema_data,
            )

    def test_delete_profile__deleted(
        self,
        document_type_service,
        fake_document_type_repository,
        document_type,
        profile_name,
        profile_schema_data,
        profile_format,
    ):
        profile_id = document_type.add_profile(profile_name, profile_schema_data, profile_format())
        fake_document_type_repository.save(document_type=document_type)
        document_type_service.delete_profile(
            document_type_id=document_type.id(),
            tenant_id=document_type.tenant_id(),
            profile_id=profile_id(),
        )

        assert len(document_type.profiles) == 1

    def test_delete_profile__doc_type_does_not_exist__raise_error(
        self, document_type_service, document_type_id, test_tenant_id, profile_id
    ):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.delete_profile(
                document_type_id=document_type_id,
                tenant_id=test_tenant_id,
                profile_id=profile_id,
            )

    def test_delete_profile__profile_does_not_exist__raise_error(
        self,
        document_type_service,
        fake_document_type_repository,
        document_type,
        test_tenant_id,
        profile_id,
    ):
        fake_document_type_repository.save(document_type=document_type)

        with pytest.raises(ProfileNotFound):
            document_type_service.delete_profile(
                document_type_id=document_type.id(),
                tenant_id=test_tenant_id,
                profile_id=profile_id,
            )

    def test_find_profiles__success(
        self, document_type_service, document_type, test_tenant_id, fake_document_type_repository
    ):
        fake_document_type_repository.save(document_type=document_type)

        profiles = document_type_service.find_profiles(document_type_id=document_type.id(), tenant_id=test_tenant_id)

        assert len(profiles) == 1
        assert isinstance(profiles[0], Profile)
