"""trainer.token_version, core FK cascades, quiz_result index (v1.36.0)

Revision ID: 75aeb8d5399c
Revises: 7305d4053e50
Create Date: 2026-07-22 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '75aeb8d5399c'
down_revision: Union[str, None] = '7305d4053e50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Trainer-Token widerrufbar, analog zu participant.token_version ---
    with op.batch_alter_table('trainer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token_version', sa.Integer(), nullable=False, server_default='0'))

    # --- Verwaiste Zeilen raeumen, BEVOR die FK-Constraints unten angelegt
    # werden. Auf einer Live-DB koennen bereits verwaiste Zeilen existieren
    # (z.B. durch fruehere manuelle Loeschungen ohne Kaskade) -- die wuerden
    # das Anlegen der Constraint sofort scheitern lassen -> Startup-Crashloop.
    # Waisen sind ohnehin toter Ballast, das Aufraeumen ist defensiv und korrekt.
    #
    # Reihenfolge wichtig: erst Kurs-Waisen raeumen (Teilnehmer/CourseModule/
    # Kommentare ohne gueltigen Kurs), DANN Teilnehmer-Waisen (Progress/Quiz/
    # Kommentare ohne gueltigen Teilnehmer) -- der erste Schritt kann durch das
    # Loeschen verwaister Teilnehmer selbst neue Waisen fuer den zweiten Schritt
    # erzeugen.
    bind = op.get_bind()
    bind.execute(sa.text("DELETE FROM participant WHERE course_id NOT IN (SELECT id FROM course)"))
    bind.execute(sa.text("DELETE FROM course_module WHERE course_id NOT IN (SELECT id FROM course)"))
    bind.execute(sa.text("DELETE FROM comment WHERE course_id NOT IN (SELECT id FROM course)"))
    bind.execute(sa.text("DELETE FROM progress WHERE participant_id NOT IN (SELECT id FROM participant)"))
    bind.execute(sa.text("DELETE FROM quiz_result WHERE participant_id NOT IN (SELECT id FROM participant)"))
    bind.execute(sa.text(
        "DELETE FROM comment WHERE participant_id IS NOT NULL "
        "AND participant_id NOT IN (SELECT id FROM participant)"
    ))

    # --- Kern-Fremdschluessel mit ON DELETE CASCADE nachruesten ---
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_participant_course_id_course', 'course', ['course_id'], ['id'], ondelete='CASCADE')
    with op.batch_alter_table('progress', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_progress_participant_id_participant', 'participant', ['participant_id'], ['id'],
            ondelete='CASCADE')
    with op.batch_alter_table('quiz_result', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_quiz_result_participant_id_participant', 'participant', ['participant_id'], ['id'],
            ondelete='CASCADE')
        # quiz_stats (trainer_modules.py) filtert immer auf module_key, teils
        # zusaetzlich per Join auf participant_id -> deckt beide Muster ab.
        batch_op.create_index(
            batch_op.f('ix_quiz_result_module_key_participant_id'), ['module_key', 'participant_id'],
            unique=False)
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_comment_course_id_course', 'course', ['course_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(
            'fk_comment_participant_id_participant', 'participant', ['participant_id'], ['id'],
            ondelete='CASCADE')
    with op.batch_alter_table('course_module', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_course_module_course_id_course', 'course', ['course_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    with op.batch_alter_table('course_module', schema=None) as batch_op:
        batch_op.drop_constraint('fk_course_module_course_id_course', type_='foreignkey')
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_comment_participant_id_participant', type_='foreignkey')
        batch_op.drop_constraint('fk_comment_course_id_course', type_='foreignkey')
    with op.batch_alter_table('quiz_result', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_quiz_result_module_key_participant_id'))
        batch_op.drop_constraint('fk_quiz_result_participant_id_participant', type_='foreignkey')
    with op.batch_alter_table('progress', schema=None) as batch_op:
        batch_op.drop_constraint('fk_progress_participant_id_participant', type_='foreignkey')
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.drop_constraint('fk_participant_course_id_course', type_='foreignkey')
    with op.batch_alter_table('trainer', schema=None) as batch_op:
        batch_op.drop_column('token_version')
