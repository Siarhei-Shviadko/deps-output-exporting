from collections import namedtuple

from deps_output_exporting.infrastructure.repositories import OutputMapper


def test_output_mapper__to_dict(output):
    expected_result = {
        "id": output.id(),
        "tenant_id": output.tenant_id(),
        "profile_info": {
            "id": output.profile_info.id(),
            "version": output.profile_info.version,
            "schema_type": output.profile_info.schema_type.value,
        },
        "document_id": output.document_id,
        "state": output.state.value,
        "file_path": output.file_path,
        "creation_date": output.creation_date,
    }

    result = OutputMapper.to_dict(output)
    assert result == expected_result


def test_output_mapper__from_row(output):
    """
    The SQLAlchemy `Row` object seeks to act as much like a Python named tuple as possible.
    """
    TestOutputRow = namedtuple(
        "TestOutputRow",
        [
            "id",
            "tenant_id",
            "profile_info",
            "document_id",
            "state",
            "file_path",
            "creation_date",
        ],
    )
    output_row = TestOutputRow(
        id=output.id(),
        tenant_id=output.tenant_id(),
        profile_info={
            "id": output.profile_info.id(),
            "version": output.profile_info.version,
            "schema_type": output.profile_info.schema_type.value,
        },
        document_id=output.document_id,
        state=output.state.value,
        file_path=output.file_path,
        creation_date=output.creation_date,
    )

    result = OutputMapper.from_row(output_row)
    assert result == output
