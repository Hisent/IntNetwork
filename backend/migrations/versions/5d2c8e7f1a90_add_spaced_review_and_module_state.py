"""review_item, warmup, warmup_result, module_state (Wiederholung, Aufwärmrunde,
serverseitiger Übungs-/Lesestand)

Rein additiv; alle Teilnehmer-Tabellen hängen per ON DELETE CASCADE am
Teilnehmer (Aufbewahrung: services/retention.py).

Revision ID: 5d2c8e7f1a90
Revises: 9f3e7a1c5b2d
Create Date: 2026-10-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5d2c8e7f1a90'
down_revision: Union[str, None] = '9f3e7a1c5b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _participant_fk():
    return sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE')


def upgrade() -> None:
    # Je Tabelle idempotent (Muster 7305d4053e50 / c8d9e0f1a2b3).
    insp = sa.inspect(op.get_bind())
    if not insp.has_table('review_item'):
        op.create_table(
            'review_item',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('participant_id', sa.Integer(), nullable=False),
            sa.Column('question_id', sa.Integer(), nullable=False),
            sa.Column('last_reviewed', sa.DateTime(), nullable=False),
            sa.Column('streak', sa.Integer(), nullable=False),
            _participant_fk(),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('participant_id', 'question_id', name='uq_review_item'),
        )
        op.create_index('ix_review_item_participant_id', 'review_item', ['participant_id'])
    if not insp.has_table('warmup'):
        op.create_table(
            'warmup',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('course_id', sa.Integer(), nullable=False),
            sa.Column('started_at', sa.DateTime(), nullable=False),
            sa.Column('ended_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_warmup_course_id', 'warmup', ['course_id'])
    if not insp.has_table('warmup_result'):
        op.create_table(
            'warmup_result',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('warmup_id', sa.Integer(), nullable=False),
            sa.Column('participant_id', sa.Integer(), nullable=False),
            sa.Column('answered', sa.Integer(), nullable=False),
            sa.Column('correct', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['warmup_id'], ['warmup.id'], ondelete='CASCADE'),
            _participant_fk(),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('warmup_id', 'participant_id', name='uq_warmup_result'),
        )
        op.create_index('ix_warmup_result_warmup_id', 'warmup_result', ['warmup_id'])
        op.create_index('ix_warmup_result_participant_id', 'warmup_result', ['participant_id'])
    if not insp.has_table('module_state'):
        op.create_table(
            'module_state',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('participant_id', sa.Integer(), nullable=False),
            sa.Column('module_key', sa.String(), nullable=False),
            sa.Column('data', sa.JSON(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            _participant_fk(),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('participant_id', 'module_key', name='uq_module_state'),
        )
        op.create_index('ix_module_state_participant_id', 'module_state', ['participant_id'])


def downgrade() -> None:
    # Kind vor Eltern (warmup_result hängt an warmup).
    insp = sa.inspect(op.get_bind())
    for table in ('module_state', 'warmup_result', 'warmup', 'review_item'):
        if insp.has_table(table):
            op.drop_table(table)
