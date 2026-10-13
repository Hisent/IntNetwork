"""content_module.goals_en (englische Lernziele)

Revision ID: b7c8d9e0f1a2
Revises: a6b7c8d9e0f1
Create Date: 2026-10-12 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b7c8d9e0f1a2'
down_revision: Union[str, None] = 'a6b7c8d9e0f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column() -> bool:
    return any(c["name"] == "goals_en" for c in sa.inspect(op.get_bind()).get_columns("content_module"))


def upgrade() -> None:
    # nullable, ohne Default: reines ADD COLUMN. Befüllt wird beim Start vom
    # Content-Sync (app/content/sync.py), sobald die Quelle goals_en trägt.
    if not _has_column():  # idempotent, siehe 75aeb8d5399c
        op.add_column("content_module", sa.Column("goals_en", sa.JSON(), nullable=True))


def downgrade() -> None:
    if _has_column():
        with op.batch_alter_table("content_module", schema=None) as batch_op:
            batch_op.drop_column("goals_en")
