"""add trainer_credential table (passkeys) (v1.34.0)

Revision ID: 7305d4053e50
Revises: e4f5a6b7c8d9
Create Date: 2026-07-22 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7305d4053e50'
down_revision: Union[str, None] = 'e4f5a6b7c8d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rein additive neue Tabelle. ondelete='CASCADE' auf trainer_id: löscht ein
    # Trainer sich, dürfen seine Passkeys nicht als verwaiste Zeilen liegen
    # bleiben (siehe app/models/trainer_credential.py für die zweite,
    # anwendungsseitige Absicherung in login/verify).
    op.create_table(
        'trainer_credential',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trainer_id', sa.Integer(), nullable=False),
        sa.Column('credential_id', sa.String(), nullable=False),
        sa.Column('public_key', sa.String(), nullable=False),
        sa.Column('sign_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('transports', sa.String(), nullable=True),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['trainer_id'], ['trainer.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('trainer_credential', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_trainer_credential_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_trainer_credential_trainer_id'), ['trainer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_trainer_credential_credential_id'), ['credential_id'], unique=True)


def downgrade() -> None:
    with op.batch_alter_table('trainer_credential', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_trainer_credential_credential_id'))
        batch_op.drop_index(batch_op.f('ix_trainer_credential_trainer_id'))
        batch_op.drop_index(batch_op.f('ix_trainer_credential_id'))
    op.drop_table('trainer_credential')
