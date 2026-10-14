"""trainer.role (admin | trainer); ältester Trainer wird admin

Revision ID: 3f9a1c7e2b40
Revises: c8d9e0f1a2b3
Create Date: 2026-10-14 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3f9a1c7e2b40'
down_revision: Union[str, None] = 'c8d9e0f1a2b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Additiv mit server_default und idempotent (Muster 75aeb8d5399c): fehlt die
    # Spalte, kommt sie dazu; Bestandszeilen werden "trainer".
    insp = sa.inspect(op.get_bind())
    if 'role' not in {c['name'] for c in insp.get_columns('trainer')}:
        with op.batch_alter_table('trainer', schema=None) as batch_op:
            batch_op.add_column(sa.Column('role', sa.String(), nullable=False, server_default='trainer'))
    # Ohne Admin könnte niemand mehr Zugänge verwalten: der älteste Trainer
    # (niedrigste id, in der Regel der per ADMIN_EMAIL geseedete) wird admin --
    # aber nur, wenn es noch keinen gibt (ein erneuter Lauf ändert nichts).
    # Leere Tabelle: nichts zu tun, seed_trainer_if_empty legt den ersten als admin an.
    op.execute(
        "UPDATE trainer SET role = 'admin' "
        "WHERE id = (SELECT MIN(id) FROM trainer) "
        "AND NOT EXISTS (SELECT 1 FROM trainer WHERE role = 'admin')"
    )


def downgrade() -> None:
    with op.batch_alter_table('trainer', schema=None) as batch_op:
        batch_op.drop_column('role')
