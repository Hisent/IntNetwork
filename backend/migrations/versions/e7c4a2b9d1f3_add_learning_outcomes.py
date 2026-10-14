"""Lernerfolg: Wissenstest vorher/nachher + anonyme Kursbewertung

course.assessment_questions/assessment_seed/assessment_phase/evaluation_open,
participant.evaluation_submitted, Tabellen assessment_answer (personenbezogen,
CASCADE am Teilnehmer) und course_evaluation (anonym, nur am Kurs).

Revision ID: e7c4a2b9d1f3
Revises: 9f3e7a1c5b2d
Create Date: 2026-10-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e7c4a2b9d1f3'
down_revision: Union[str, None] = '9f3e7a1c5b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def _course_columns() -> list[sa.Column]:
    return [sa.Column("assessment_questions", sa.JSON(), nullable=True),
            sa.Column("assessment_seed", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("assessment_phase", sa.String(), nullable=True),
            sa.Column("evaluation_open", sa.Boolean(), nullable=False, server_default=sa.false())]


def _columns(table: str) -> set[str]:
    return {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    # Je Spalte/Tabelle idempotent (Muster 75aeb8d5399c / 7305d4053e50).
    have = _columns("course")
    with op.batch_alter_table("course", schema=None) as batch_op:
        for col in _course_columns():
            if col.name not in have:
                batch_op.add_column(col)
    if "evaluation_submitted" not in _columns("participant"):
        with op.batch_alter_table("participant", schema=None) as batch_op:
            batch_op.add_column(sa.Column("evaluation_submitted", sa.Boolean(), nullable=False,
                                          server_default=sa.false()))
    insp = sa.inspect(op.get_bind())
    if not insp.has_table("assessment_answer"):
        op.create_table(
            "assessment_answer",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("participant_id", sa.Integer(), nullable=False),
            sa.Column("phase", sa.String(), nullable=False),
            sa.Column("answers", sa.JSON(), nullable=False),
            sa.Column("score", sa.Integer(), nullable=False),
            sa.Column("total", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["participant_id"], ["participant.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("participant_id", "phase", name="uq_assessment_answer"),
        )
        op.create_index("ix_assessment_answer_participant_id", "assessment_answer", ["participant_id"])
    if not insp.has_table("course_evaluation"):
        op.create_table(
            "course_evaluation",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("course_id", sa.Integer(), nullable=False),
            sa.Column("overall", sa.Integer(), nullable=False),
            sa.Column("clarity", sa.Integer(), nullable=True),
            sa.Column("practice", sa.Integer(), nullable=True),
            sa.Column("pace", sa.String(), nullable=True),
            sa.Column("trainer", sa.Integer(), nullable=True),
            sa.Column("good", sa.Text(), nullable=True),
            sa.Column("improve", sa.Text(), nullable=True),
            sa.ForeignKeyConstraint(["course_id"], ["course.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_course_evaluation_course_id", "course_evaluation", ["course_id"])


def downgrade() -> None:
    insp = sa.inspect(op.get_bind())
    for table in ("course_evaluation", "assessment_answer"):
        if insp.has_table(table):
            op.drop_table(table)
    if "evaluation_submitted" in _columns("participant"):
        with op.batch_alter_table("participant", schema=None) as batch_op:
            batch_op.drop_column("evaluation_submitted")
    have = _columns("course")
    with op.batch_alter_table("course", schema=None) as batch_op:
        for col in reversed(_course_columns()):
            if col.name in have:
                batch_op.drop_column(col.name)
