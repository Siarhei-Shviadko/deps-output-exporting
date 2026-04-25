import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from deps_output_exporting.entrypoint import create_fastapi


@pytest.fixture(scope="session")
def app() -> FastAPI:
    fastapi_app = create_fastapi()
    yield fastapi_app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def session_containers(app):
    return app.containers


@pytest.fixture
def containers(session_containers):
    with session_containers.reset_singletons():
        yield session_containers


@pytest.fixture
def repositories(containers):
    return containers.repositories


@pytest.fixture
def external_services(containers):
    return containers.external_services


@pytest.fixture
def document_type_proxy(external_services):
    with external_services.reset_singletons():
        return external_services.document_type_proxy()
