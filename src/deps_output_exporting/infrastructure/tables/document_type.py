from sqlalchemy import Column, PrimaryKeyConstraint, String, Table, UniqueConstraint

from deps_output_exporting.extras.datasource import metadata

__all__ = ["document_type_table"]
document_type_table = Table(
    "document_type",
    metadata,
    Column("id", String, primary_key=True),
    Column("tenant_id", String, nullable=False),
    UniqueConstraint("id", "tenant_id", name="document_type_id_tenant_id_unique"),
)
