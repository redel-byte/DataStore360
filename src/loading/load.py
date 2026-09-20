from pathlib import Path
import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection
from sqlalchemy.engine import Engine

SCHEMA_SQL_PATH = Path(
    "/mnt/c/Users/Youcode/Documents/DEV_AI/sprint_1/DataStore360/sql/01_create_schemas.sql"
)
DEFAULT_DATASET_PATH = (
    "/mnt/c/Users/Youcode/Documents/DEV_AI/sprint_1/DataStore360/data/raw/store_data.csv"
)

REQUIRED_SCHEMAS = ("staging", "core")

STAGING_COLUMNS = {
    "Row ID": "row_id",
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Ship Date": "ship_date",
    "Ship Mode": "ship_mode",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Segment": "segment",
    "Country": "country",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Region": "region",
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
    "Sales": "sales",
    "Quantity": "quantity",
    "Discount": "discount",
    "Profit": "profit",
}

EXPECTED_COLUMNS = list(STAGING_COLUMNS.values())


def execute_sql_file(connection: Connection, sql_path: Path) -> None:
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    sql = sql_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
    for statement in statements:
        connection.execute(text(statement))


def ensure_database_schemas(engine: Engine, sql_path: Path = SCHEMA_SQL_PATH) -> None:
    with engine.begin() as connection:
        inspector = inspect(connection)

        if all(inspector.has_schema(schema) for schema in REQUIRED_SCHEMAS):
            return

        execute_sql_file(connection, sql_path)

        inspector = inspect(connection)
        missing_schemas = [
            schema for schema in REQUIRED_SCHEMAS if not inspector.has_schema(schema)
        ]
        if missing_schemas:
            raise RuntimeError(f"Failed to create required schemas: {missing_schemas}")


def process_column_names(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("[!] empty DataFrame.")

    staging_df = df.rename(columns=STAGING_COLUMNS)
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in staging_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required staging columns: {missing_columns}")

    return staging_df[EXPECTED_COLUMNS].copy()


def load_to_staging(df: pd.DataFrame, engine: Engine) -> None:
    staging_df = process_column_names(df)

    with engine.begin() as connection:
        inspector = inspect(connection)
        if inspector.has_table("superstore_raw", schema="staging"):
            connection.execute(text(f"TRUNCATE TABLE staging.superstore_raw"))

        staging_df.to_sql(
            name="superstore_raw",
            con=connection,
            schema="staging",
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1000,
        )


def main() -> None:
    from src.config.database import engine
    from src.extraction.extracte import extracte

    df = extracte(DEFAULT_DATASET_PATH)
    ensure_database_schemas(engine)
    load_to_staging(df, engine)


if __name__ == "__main__":
    main()
