"""Live-Steuerung: course.follow_* („Folgt mir“) + participant.module_entered_at („Wer hängt fest?“)

Rein additiv, alle Spalten nullable — Bestandszeilen bleiben gültig.

Revision ID: 5e7f0a1b2c3d
Revises: 9f3e7a1c5b2d
Create Date: 2026-10-14 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5e7f0a1b2c3d'
down_revision: Union[str, None] = '9f3e7a1c5b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_COLUMNS = {
    "course": [("follow_module_key", sa.String()), ("follow_block_uid", sa.String()),
               ("follow_updated_at", sa.DateTime())],
    "participant": [("module_entered_at", sa.DateTime())],
}


def _columns(table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    # Je Spalte idempotent (Muster 75aeb8d5399c).
    for table, cols in _COLUMNS.items():
        have = _columns(table)
        with op.batch_alter_table(table, schema=None) as batch_op:
            for name, type_ in cols:
                if name not in have:
                    batch_op.add_column(sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    for table, cols in _COLUMNS.items():
        have = _columns(table)
        with op.batch_alter_table(table, schema=None) as batch_op:
            for name, _type in reversed(cols):
                if name in have:
                    batch_op.drop_column(name)
