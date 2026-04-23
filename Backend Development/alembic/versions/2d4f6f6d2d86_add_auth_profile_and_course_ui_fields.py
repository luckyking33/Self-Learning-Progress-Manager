"""add auth profile and course ui fields"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "2d4f6f6d2d86"
down_revision = "9b1f0d6b0c25"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("avatar", sa.String(length=16), server_default="ST", nullable=False),
    )
    op.add_column(
        "users",
        sa.Column(
            "headline",
            sa.String(length=255),
            server_default="Learning with STAR",
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column("streak_days", sa.Integer(), server_default=sa.text("0"), nullable=False),
    )

    op.add_column(
        "courses",
        sa.Column("subtitle", sa.String(length=255), server_default="", nullable=False),
    )
    op.add_column(
        "courses",
        sa.Column(
            "tags",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )
    op.add_column(
        "courses",
        sa.Column("category", sa.String(length=50), server_default="CS自学", nullable=False),
    )
    op.add_column(
        "courses",
        sa.Column(
            "cover_tone",
            sa.String(length=255),
            server_default="from-sky-100 via-white to-cyan-50",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("courses", "cover_tone")
    op.drop_column("courses", "category")
    op.drop_column("courses", "tags")
    op.drop_column("courses", "subtitle")
    op.drop_column("users", "streak_days")
    op.drop_column("users", "headline")
    op.drop_column("users", "avatar")
