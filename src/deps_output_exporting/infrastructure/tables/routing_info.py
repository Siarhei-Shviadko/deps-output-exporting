from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, String, Table

from deps_output_exporting.extras.datasource import metadata

__all__ = ["routing_info_table"]

routing_info_table = Table(
    "routing_info",
    metadata,
    Column("tenant_id", String, primary_key=True),
    Column(
        "document_type_id",
        ForeignKey("document_type.id", ondelete="cascade", name="document_type_id_fkey"),
        primary_key=True,
    ),
    Column(
        "profile_id",
        ForeignKey("profile.id", ondelete="cascade", name="profile_id_fkey"),
        primary_key=True,
    ),
    Column("command_channel", String, nullable=False),
    PrimaryKeyConstraint(
        "tenant_id",
        "document_type_id",
        "profile_id",
        name="tenant_id__document_type_id__profile_id__pk",
    ),
)
