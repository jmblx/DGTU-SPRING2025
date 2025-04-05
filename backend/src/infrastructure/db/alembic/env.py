import os
import sys
from logging.config import fileConfig

from core.config import config_loader
from infrastructure.db.models import Base
from sqlalchemy import create_engine

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

config = context.config

db_config = config_loader.app_config.database

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", db_config.host)
config.set_section_option(section, "DB_PORT", db_config.port)
config.set_section_option(section, "DB_USER", db_config.user)
config.set_section_option(section, "DB_NAME", db_config.name)
config.set_section_option(section, "DB_PASS", db_config.password)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = config.get_main_option("sqlalchemy.url")

    # Заменяем asyncpg → psycopg2 только в тестах
    if os.getenv("TESTING") == "true" and "asyncpg" in url:
        url = url.replace("asyncpg", "psycopg2").split("?")[0]

    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
