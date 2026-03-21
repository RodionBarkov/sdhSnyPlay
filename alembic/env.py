from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine

from database import Model  # <-- ваш DeclarativeBase

config = context.config
fileConfig(config.config_file_name)

target_metadata = Model.metadata
# (опционально) поможет автодетекту отличий типов
# compare_type = True задайте в context.configure ниже

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    connectable = create_engine(configuration["sqlalchemy.url"])

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    # можно оставить дефолтный run_migrations_offline()
    ...
else:
    run_migrations_online()