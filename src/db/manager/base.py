from abc import ABC, abstractmethod
from psycopg2 import extensions
from src.config import settings


class DBManager(ABC):
    def __init__(self, db_name: str = settings.DB_NAME):
        self.db_name = db_name
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.host = settings.DB_HOST
        self.port = settings.DB_PORT
        self.connection: extensions.connection | None = None

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    def commit(self) -> None:
        self.connection.commit()
