from src.db.manager import PostgresDBManager
from src.config import settings


def create_database() -> None:
    db_manager = PostgresDBManager(db_name='postgres')
    db_manager.connect()
    db_manager.connection.autocommit = True

    try:
        with db_manager.connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {settings.DB_NAME}")
            cursor.execute(f"CREATE DATABASE {settings.DB_NAME}")

        db_manager.commit()

    finally:
        db_manager.disconnect()


def apply_migrations():
    db_manager = PostgresDBManager()
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for migration in sorted(settings.MIGRATION_DIR.glob('*.sql')):
                cursor.execute(_read_migrations(migration))

            db_manager.commit()

    finally:
        db_manager.disconnect()


def _read_migrations(file_path) -> str:
    with file_path.open(encoding='utf-8') as f:
        return f.read()
