from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from deps_output_exporting.extras.datasource import metadata

__all__ = ["output_table"]

output_table = Table(
    "output",
    metadata,
    Column("id", String, primary_key=True),
    Column(
        "tenant_id",
        String,
        nullable=False,
    ),
    Column("profile_info", JSONB, nullable=False),
    Column("document_id", String, nullable=False),
    Column("state", String, nullable=False),
    Column("file_path", String, nullable=True),
    Column("creation_date", DateTime, nullable=False),
)
