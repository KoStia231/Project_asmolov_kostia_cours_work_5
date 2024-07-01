import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()


class Settings:
    """Класс для настроек подключения"""
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    EMPLOYEE_IDS_CONFIG_PATH = BASE_DIR.joinpath("employers_config.json")
    MIGRATION_DIR = BASE_DIR.joinpath('src', 'migrations')

    def get_employee_ids(self) -> list[int]:
        with self.EMPLOYEE_IDS_CONFIG_PATH.open() as file:
            data = json.load(file)

        return data["employers"]["hh"]


settings = Settings()
