from random import choice
from uuid import uuid4

import pytest

from deps_output_exporting.domain.model import (
    DocumentTypeFactory,
    EntityId,
    Output,
    OutputState,
    ProfileInfo,
    RoutingInfo,
    SchemaType,
    TenantId,
)


@pytest.fixture(autouse=True)
def session(containers):
    database = containers.datasources.postgres_datasource()
    connection = database.get_connection()

    class TrapForThreadLocalConnections:
        """
        This class is used instead of threading.local in Database, for allowing connection transactions management
        """

        connection = None

    TrapForThreadLocalConnections.connection = connection
    transaction = connection.begin_nested()
    database._registry = TrapForThreadLocalConnections
    try:
        yield
    finally:
        transaction.rollback()
    database.close()


@pytest.fixture
def document_type_repository(repositories):
    return repositories.document_type()


@pytest.fixture
def test_tenant_id():
    return uuid4().hex


@pytest.fixture
def document_type_id():
    return uuid4().hex


@pytest.fixture
def document_type(document_type_id, test_tenant_id):
    return DocumentTypeFactory.create(document_type_id, test_tenant_id)


@pytest.fixture
def output_repository(repositories):
    return repositories.output()


@pytest.fixture
def routing_info_repository(repositories):
    return repositories.routing_info()


@pytest.fixture
def profile_info():
    return ProfileInfo(
        id_=EntityId(uuid4().hex),
        version=uuid4().hex,
        schema_type=choice(list(SchemaType)),
    )


@pytest.fixture
def output(profile_info, test_tenant_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info,
        document_id=str(faker.random_int()),
        state=OutputState.PENDING,
        file_path=faker.file_path(),
    )


@pytest.fixture
def output_updated_state(output):
    return Output(
        id_=EntityId(output.id()),
        tenant_id=TenantId(output.tenant_id()),
        profile_info=output.profile_info,
        document_id=output.document_id,
        state=OutputState.READY,
        file_path=output.file_path,
    )


@pytest.fixture
def profile_info2():
    return ProfileInfo(
        id_=EntityId(uuid4().hex),
        version=uuid4().hex,
        schema_type=choice(list(SchemaType)),
    )


@pytest.fixture
def output2(profile_info2, test_tenant_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info2,
        document_id=str(faker.random_int()),
        state=choice([OutputState.READY, OutputState.PENDING]),
        file_path=faker.file_path(),
    )


@pytest.fixture
def document_type__new_default_profile(document_type_id, test_tenant_id):
    return DocumentTypeFactory.create(document_type_id, test_tenant_id)


@pytest.fixture
def new_output_of_profile(output, test_tenant_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=output.profile_info,
        document_id=output.document_id,
        state=OutputState.PENDING,
        file_path=faker.file_path(),
    )


@pytest.fixture
def new_output_another_profile(output, profile_info2, test_tenant_id, faker):
    return Output(
        id_=EntityId(uuid4().hex),
        tenant_id=TenantId(test_tenant_id),
        profile_info=profile_info2,
        document_id=output.document_id,
        state=OutputState.PENDING,
        file_path=faker.file_path(),
    )


@pytest.fixture
def routing_info(profile_info, document_type):
    default_profile_id = list(document_type.profiles.keys())[0]
    return RoutingInfo(
        tenant_id=document_type.tenant_id,
        document_type_id=document_type.id,
        profile_id=EntityId(default_profile_id),
        command_channel=uuid4().hex,
    )
