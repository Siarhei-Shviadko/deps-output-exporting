from datetime import datetime
from uuid import uuid4

import pytest
from dependency_injector.providers import deepcopy

from deps_output_exporting.infrastructure import (
    DocumentDetail,
    SerializedDocumentType,
    SerializedExtractedData,
    SerializedUnifiedData,
    SerializedValidationResult,
)
from deps_output_exporting.messaging.commands import BuildOutput
from tests.data import (
    document_detail_dict,
    document_type_dict,
    extracted_data_dict,
    unified_data_dict,
    validation_result_dict,
)
from tests.fakes import (
    FakeDocumentProxy,
    FakeDocumentTypeProxy,
    FakeExtractionProxy,
    FakeUnifierProxy,
    FakeValidationProxy,
)


@pytest.fixture
def output_id():
    return uuid4().hex


@pytest.fixture
def fake_document_proxy_with_document_detail(fake_document_proxy: FakeDocumentProxy, document_id):
    fake_document_proxy.document_details[document_id] = DocumentDetail(
        title=document_detail_dict["title"],
        date=datetime.fromisoformat(document_detail_dict["date"]),
        engine=document_detail_dict["engine"],
    )


@pytest.fixture
def fake_extraction_proxy_with_extracted_data(fake_extraction_proxy: FakeExtractionProxy, document_id):
    extracted_data = deepcopy(extracted_data_dict)
    extracted_data["documentId"] = document_id
    fake_extraction_proxy.extracted_data[document_id] = SerializedExtractedData.model_validate(
        extracted_data
    ).to_model()


@pytest.fixture
def fake_document_type_proxy_with_document_type(fake_document_type_proxy: FakeDocumentTypeProxy, document_type_id):
    document_type = deepcopy(document_type_dict)
    document_type["id"] = document_type_id
    fake_document_type_proxy.document_types[document_type_id] = SerializedDocumentType.model_validate(
        document_type
    ).to_model()


@pytest.fixture
def fake_unifier_proxy_with_unify_data(fake_unifier_proxy: FakeUnifierProxy, document_id):
    unified_data = deepcopy(unified_data_dict)
    unified_data["documentId"] = document_id
    fake_unifier_proxy.unified_data[document_id] = SerializedUnifiedData.model_validate(unified_data).to_model()


@pytest.fixture
def fake_validation_proxy_with_validation_info(fake_validation_proxy: FakeValidationProxy, document_id):
    fake_validation_proxy.validation_info[document_id] = SerializedValidationResult.model_validate(
        validation_result_dict
    ).to_model()


@pytest.fixture
def build_output_message(cmm, document_type_id, profile_id, document_id, output_id):
    cmm.command = BuildOutput(
        document_id=document_id,
        document_type_id=document_type_id,
        profile_id=profile_id,
        output_id=output_id,
    )

    return cmm
