"""add audit_log table (v1.22.0)

Revision ID: d3e4f5a6b7c8
Revises: c2d3e4f5a6b7
Create Date: 2026-07-21 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd3e4f5a6b7c8'
down_revision: Union[str, None] = 'c2d3e4f5a6b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Idempotent, aus demselben Grund wie 7305d4053e50 (Vorfall 22.07.2026):
    # app/main.py rief frueher nach run_migrations() zusaetzlich
    # Base.metadata.create_all() auf. Das legt fehlende Tabellen an, OHNE dass
    # Alembic davon erfaehrt -- steht alembic_version danach noch auf der
    # Vorgaenger-Revision, scheitert dieser Schritt beim naechsten Start an
    # "relation already exists" -- der Prozess stirbt, die Plattform startet
    # neu, endlos. Existiert die Tabelle bereits, wird sie hier uebersprungen.
    if sa.inspect(op.get_bind()).has_table('audit_log'):
        return

    # Rein additive neue Tabelle, bewusst ohne Fremdschlüssel (siehe
    # app/models/audit_log.py) -> Einträge überleben Trainer-/Teilnehmer-Löschungen.
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('trainer_id', sa.Integer(), nullable=True),
        sa.Column('trainer_email', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('target', sa.String(), nullable=True),
        sa.Column('detail', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('audit_log', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_audit_log_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_audit_log_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_audit_log_action'), ['action'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('audit_log', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_audit_log_action'))
        batch_op.drop_index(batch_op.f('ix_audit_log_created_at'))
        batch_op.drop_index(batch_op.f('ix_audit_log_id'))
    op.drop_table('audit_log')
