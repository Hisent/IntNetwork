"""add course.require_approval and participant.approved (v1.21.0)

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-07-20 21:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c2d3e4f5a6b7'
down_revision: Union[str, None] = 'b1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Additiv mit server_default, damit Bestandszeilen einen definierten Wert bekommen.
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('require_approval', sa.Boolean(), nullable=False, server_default='0'))
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved', sa.Boolean(), nullable=False, server_default='0'))


def downgrade() -> None:
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.drop_column('approved')
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('require_approval')
