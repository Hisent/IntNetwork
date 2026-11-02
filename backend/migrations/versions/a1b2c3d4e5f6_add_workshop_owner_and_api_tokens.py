"""workshop.status/owner_trainer_id + trainer_api_token (MCP-Lehrgangsautoren)

Revision ID: a1b2c3d4e5f6
Revises: 9f3e7a1c5b2d
Create Date: 2026-11-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '9f3e7a1c5b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_FK = 'fk_workshop_owner_trainer_id_trainer'


# Idempotent wie 75aeb8d5399c: Objekte koennen durch create_all/manuelle
# Reparaturen schon existieren, ohne dass alembic_version davon weiss.
def _has_column(insp, table: str, column: str) -> bool:
    return any(c["name"] == column for c in insp.get_columns(table))


def _has_fk(insp, table: str, name: str) -> bool:
    return any(fk["name"] == name for fk in insp.get_foreign_keys(table))


def _has_index(insp, table: str, name: str) -> bool:
    return any(ix["name"] == name for ix in insp.get_indexes(table))


def upgrade() -> None:
    insp = sa.inspect(op.get_bind())

    if not _has_column(insp, 'workshop', 'status'):
        with op.batch_alter_table('workshop', schema=None) as batch_op:
            batch_op.add_column(sa.Column('status', sa.String(), nullable=False, server_default='published'))
    if not _has_column(insp, 'workshop', 'owner_trainer_id'):
        with op.batch_alter_table('workshop', schema=None) as batch_op:
            batch_op.add_column(sa.Column('owner_trainer_id', sa.Integer(), nullable=True))
    if not _has_fk(insp, 'workshop', _FK):
        with op.batch_alter_table('workshop', schema=None) as batch_op:
            batch_op.create_foreign_key(_FK, 'trainer', ['owner_trainer_id'], ['id'], ondelete='SET NULL')

    if not insp.has_table('trainer_api_token'):
        op.create_table(
            'trainer_api_token',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('trainer_id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('token_hash', sa.String(), nullable=False),
            sa.Column('prefix', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('last_used_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['trainer_id'], ['trainer.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('token_hash'),
        )
        insp = sa.inspect(op.get_bind())
    for name, cols in (('ix_trainer_api_token_id', ['id']), ('ix_trainer_api_token_trainer_id', ['trainer_id'])):
        if not _has_index(insp, 'trainer_api_token', name):
            with op.batch_alter_table('trainer_api_token', schema=None) as batch_op:
                batch_op.create_index(batch_op.f(name), cols, unique=False)


def downgrade() -> None:
    with op.batch_alter_table('trainer_api_token', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_trainer_api_token_trainer_id'))
        batch_op.drop_index(batch_op.f('ix_trainer_api_token_id'))
    op.drop_table('trainer_api_token')
    with op.batch_alter_table('workshop', schema=None) as batch_op:
        batch_op.drop_constraint(_FK, type_='foreignkey')
        batch_op.drop_column('owner_trainer_id')
        batch_op.drop_column('status')
