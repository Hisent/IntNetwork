"""add certificate table and participant.resume_code (v1.19.0)

Revision ID: b1c2d3e4f5a6
Revises: 7a63b63c8cde
Create Date: 2026-07-20 20:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, None] = '7a63b63c8cde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rein additiv -> auch auf adoptierten Bestands-DBs (Postgres) risikoarm.
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('resume_code', sa.String(), nullable=True))

    op.create_table(
        'certificate',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('participant_name', sa.String(), nullable=False),
        sa.Column('course_name', sa.String(), nullable=False),
        sa.Column('workshop_title', sa.String(), nullable=False),
        sa.Column('module_count', sa.Integer(), nullable=False),
        sa.Column('issued_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('certificate', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_certificate_participant_id'), ['participant_id'], unique=True)


def downgrade() -> None:
    with op.batch_alter_table('certificate', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_certificate_participant_id'))
    op.drop_table('certificate')
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.drop_column('resume_code')
