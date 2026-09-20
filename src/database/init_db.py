from pathlib import Path
from sqlalchemy import text
from src.config.database import engine

SQL_PATH = Path("/sql/01_create_schemas.sql")


def create_schemas() -> None:

    sql = SQL_PATH.read_text(encoding="utf-8")

    with engine.begin() as connection:
        connection.execute(text(sql))


if __name__ == "__main__":
    create_schemas()
    print("Schemas created successfully.")
