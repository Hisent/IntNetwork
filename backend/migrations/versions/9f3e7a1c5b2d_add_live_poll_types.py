"""live_poll.kind/config + live_poll_vote.value/hidden (Abstimmungsarten)

Mehrfachauswahl, Skala, Freitext und Wortwolke. Bestehende Abstimmungen sind
kind="single" (server_default), ihre Stimmen bleiben in choice.

Revision ID: 9f3e7a1c5b2d
Revises: c8d9e0f1a2b3
Create Date: 2026-10-14 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9f3e7a1c5b2d'
down_revision: Union[str, None] = 'c8d9e0f1a2b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _columns(table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    # Je Spalte idempotent (Muster 75aeb8d5399c).
    have = _columns("live_poll")
    with op.batch_alter_table("live_poll", schema=None) as batch_op:
        if "kind" not in have:
            batch_op.add_column(sa.Column("kind", sa.String(), nullable=False, server_default="single"))
        if "config" not in have:
            batch_op.add_column(sa.Column("config", sa.JSON(), nullable=True))
    have = _columns("live_poll_vote")
    with op.batch_alter_table("live_poll_vote", schema=None) as batch_op:
        if "value" not in have:
            batch_op.add_column(sa.Column("value", sa.JSON(), nullable=True))
        if "hidden" not in have:
            batch_op.add_column(sa.Column("hidden", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.alter_column("choice", existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    # Abstimmungen der neuen Arten kennt das alte Schema nicht: Stimmen zuerst
    # (SQLite kaskadiert ohne PRAGMA foreign_keys nicht), dann die Abstimmungen.
    op.execute("DELETE FROM live_poll_vote WHERE choice IS NULL "
               "OR poll_id IN (SELECT id FROM live_poll WHERE kind <> 'single')")
    op.execute("DELETE FROM live_poll WHERE kind <> 'single'")
    have = _columns("live_poll_vote")
    with op.batch_alter_table("live_poll_vote", schema=None) as batch_op:
        for col in ("hidden", "value"):
            if col in have:
                batch_op.drop_column(col)
        batch_op.alter_column("choice", existing_type=sa.Integer(), nullable=False)
    have = _columns("live_poll")
    with op.batch_alter_table("live_poll", schema=None) as batch_op:
        for col in ("config", "kind"):
            if col in have:
                batch_op.drop_column(col)
