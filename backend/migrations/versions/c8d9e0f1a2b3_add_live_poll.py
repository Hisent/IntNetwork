"""live_poll + live_poll_vote (Live-Abstimmung im Präsenz-Workshop)

Revision ID: c8d9e0f1a2b3
Revises: b7c8d9e0f1a2
Create Date: 2026-10-13 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c8d9e0f1a2b3'
down_revision: Union[str, None] = 'b7c8d9e0f1a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rein additiv und je Tabelle idempotent (Muster 7305d4053e50): existiert
    # eine Tabelle schon, wird sie übersprungen statt an "already exists" zu sterben.
    insp = sa.inspect(op.get_bind())
    if not insp.has_table('live_poll'):
        op.create_table(
            'live_poll',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('course_id', sa.Integer(), nullable=False),
            sa.Column('module_key', sa.String(), nullable=False),
            sa.Column('source', sa.String(), nullable=False),
            sa.Column('ref', sa.String(), nullable=False),
            sa.Column('status', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_live_poll_course_id', 'live_poll', ['course_id'])
    if not insp.has_table('live_poll_vote'):
        op.create_table(
            'live_poll_vote',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('poll_id', sa.Integer(), nullable=False),
            sa.Column('participant_id', sa.Integer(), nullable=False),
            sa.Column('choice', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['poll_id'], ['live_poll.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('poll_id', 'participant_id', name='uq_live_poll_vote'),
        )
        op.create_index('ix_live_poll_vote_poll_id', 'live_poll_vote', ['poll_id'])
        op.create_index('ix_live_poll_vote_participant_id', 'live_poll_vote', ['participant_id'])


def downgrade() -> None:
    op.drop_table('live_poll_vote')
    op.drop_table('live_poll')
