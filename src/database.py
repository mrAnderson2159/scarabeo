from json import dumps, loads
from pathlib import Path

DB_PATH = Path("../database/database.json")


class Database:
    @staticmethod
    def load():
        if DB_PATH.exists():
            with open(DB_PATH, "r") as file:
                return loads(file.read())
        else:
            raise FileNotFoundError(f"Database file not found at {DB_PATH}")

    @staticmethod
    def save(data):
        with open(DB_PATH, "w") as file:
            file.write(dumps(data))
