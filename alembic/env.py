from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.infrastructure.config import configuracoes
from app.infrastructure.database import Base
from app.infrastructure.models import venda  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Utiliza a URL definida nas configurações da aplicação.
config.set_main_option(
    "sqlalchemy.url",
    configuracoes.database_url.replace("%", "%%"),
)

# Metadados utilizados pelo Alembic para identificar os modelos.
target_metadata = Base.metadata


def executar_migrations_offline() -> None:
    url = configuracoes.database_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def executar_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as conexao:
        context.configure(
            connection=conexao,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    executar_migrations_offline()
else:
    executar_migrations_online()
