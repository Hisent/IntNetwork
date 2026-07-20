from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

from app.config import settings
from app.database import Base

# Alle Modelle importieren, damit Base.metadata für --autogenerate vollständig ist.
# Bewusst NICHT app.main importieren (das würde den Startup-Seed auslösen).
from app.models import course as _course  # noqa: F401
from app.models import course_module as _course_module  # noqa: F401
from app.models import participant as _participant  # noqa: F401
from app.models import progress as _progress  # noqa: F401
from app.models import quiz_result as _quiz_result  # noqa: F401
from app.models import module_disabled as _module_disabled  # noqa: F401
from app.models import setting as _setting  # noqa: F401
from app.models import comment as _comment  # noqa: F401
from app.models import content as _content  # noqa: F401
from app.models import workshop as _workshop  # noqa: F401
from app.models import trainer as _trainer  # noqa: F401
from app.models import certificate as _certificate  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url, target_metadata=target_metadata,
        literal_binds=True, render_as_batch=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(settings.database_url)
    with connectable.connect() as connection:
        # render_as_batch=True: SQLite kennt kein natives ALTER — Batch-Modus baut
        # Tabellen bei Änderungen sauber um. Auf Postgres ein No-op.
        context.configure(connection=connection, target_metadata=target_metadata,
                          render_as_batch=True)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
