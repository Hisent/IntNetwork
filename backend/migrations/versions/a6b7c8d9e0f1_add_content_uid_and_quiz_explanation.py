"""content_block.uid, content_quiz_question.uid/explanation_de/explanation_en (v1.43.0)

Revision ID: a6b7c8d9e0f1
Revises: 75aeb8d5399c
Create Date: 2026-10-12 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a6b7c8d9e0f1'
down_revision: Union[str, None] = '75aeb8d5399c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Alle Spalten nullable und ohne Default: reines ADD COLUMN, kein Tabellen-Rewrite.
# Die Kennungen (uid) der Bestandszeilen füllt der Content-Sync beim Start
# (app/content/sync.py, _assign_missing_uids).
_COLUMNS = [
    ('content_block', 'uid', sa.String()),
    ('content_quiz_question', 'uid', sa.String()),
    ('content_quiz_question', 'explanation_de', sa.Text()),
    ('content_quiz_question', 'explanation_en', sa.Text()),
]


def _has_column(table: str, column: str) -> bool:
    return any(c["name"] == column for c in sa.inspect(op.get_bind()).get_columns(table))


def upgrade() -> None:
    for table, column, type_ in _COLUMNS:
        if not _has_column(table, column):  # idempotent, siehe 75aeb8d5399c
            op.add_column(table, sa.Column(column, type_, nullable=True))


def downgrade() -> None:
    # Mit den Spalten geht Inhalt verloren (die Erklärungen); die gespeicherten
    # Sync-Hashes (app/content/sync.py, HASH_KEY) passen dann zu keinem Modul
    # mehr und jedes gälte dauerhaft als "vom Trainer geändert". Ohne Hash
    # greift wieder die Bootstrap-Regel des Syncs.
    op.execute("DELETE FROM setting WHERE key LIKE 'content-sync:%'")
    for table, column, _type in reversed(_COLUMNS):
        if _has_column(table, column):
            with op.batch_alter_table(table, schema=None) as batch_op:
                batch_op.drop_column(column)
