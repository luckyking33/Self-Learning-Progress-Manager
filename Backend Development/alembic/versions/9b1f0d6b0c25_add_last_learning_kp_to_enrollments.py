"""add last learning knowledge point to enrollments"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "9b1f0d6b0c25"
down_revision = "760dc0558cf4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "enrollments",
        sa.Column("last_learning_knowledge_point_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        op.f("fk_enrollments_last_learning_knowledge_point_id_knowledge_points"),
        "enrollments",
        "knowledge_points",
        ["last_learning_knowledge_point_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_enrollments_last_learning_knowledge_point_id_knowledge_points"),
        "enrollments",
        type_="foreignkey",
    )
    op.drop_column("enrollments", "last_learning_knowledge_point_id")
