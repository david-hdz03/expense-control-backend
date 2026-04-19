from logging.config import fileConfig

<<<<<<< HEAD
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import settings
from app.db.base import Base
from app.models import Expense, OAuthAccount, User  # noqa: F401 — register mappers

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with the one from our settings (.env).
if settings.database_url:
    config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
=======
from sqlalchemy import engine_from_config, pool

from alembic import context
from core.config import settings
from db.all_models import (
    SQLModel,  # noqa: F401 — importa all_models para registrar los modelos
)

config = context.config

section = config.config_ini_section
config.set_section_option(
    section,
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
>>>>>>> 72a6b47fbe6208f95054d664927bf93918082bae
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
<<<<<<< HEAD

=======
>>>>>>> 72a6b47fbe6208f95054d664927bf93918082bae
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
<<<<<<< HEAD
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
=======
>>>>>>> 72a6b47fbe6208f95054d664927bf93918082bae
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
<<<<<<< HEAD
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

=======
        context.configure(connection=connection, target_metadata=target_metadata)
>>>>>>> 72a6b47fbe6208f95054d664927bf93918082bae
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
