from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from deps_output_exporting.extras.datasource import metadata

__all__ = ["profile_table"]

profile_table = Table(
    "profile",
    metadata,
    Column("id", String, primary_key=True),
    Column(
        "document_type_id",
        ForeignKey("document_type.id", ondelete="cascade", name="profile_document_type_id_fkey"),
        nullable=False,
    ),
    Column("name", String, nullable=False),
    Column("creation_date", DateTime, nullable=False),
    Column("schema", JSONB, nullable=True),
    Column("version", String, nullable=False),
    Column("format", String, nullable=False),
    Column("external_storages_info", JSONB, nullable=True),
    Column("exporting_type", String, nullable=False),
)
