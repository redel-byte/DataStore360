from pathlib import Path
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

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
PRODUCT_COLUMN_MAPPING = {
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
}
PRODUCT_COLUMNS = tuple(PRODUCT_COLUMN_MAPPING.values())
CLEAN_DATASET_PATH = "../../data/profiling/clean_store_data.csv"


def read_products_from_clean_file(CLEAN_DATASET_PATH) -> pd.DataFrame:
    clean_dataset_path = Path(CLEAN_DATASET_PATH)
    if not clean_dataset_path.exists():
        raise FileNotFoundError(f"Clean dataset not found: {clean_dataset_path}")

    return pd.read_csv(clean_dataset_path, encoding="utf-8")


def prepare_products(clean_df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [
        column for column in PRODUCT_COLUMN_MAPPING if column not in clean_df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing product columns: {missing_columns}")
    .r
    df = clean_df.rename(columns=STAGING_COLUMNS)
    products = df[PRODUCT_COLUMN_MAPPING]

    return products


def load_products_to_core(
    engine: Engine,
    clean_dataset_path: Path = CLEAN_DATASET_PATH,
) -> int:
    products = prepare_products(read_products_from_clean_file(clean_dataset_path))
    if products.empty:
        return 0

    metadata = MetaData()
    products_table = Table("products", metadata, schema="core", autoload_with=engine)
    records = products.astype(object).where(products.notna(), None).to_dict("records")

    statement = insert(products_table).values(records)
    statement = statement.on_conflict_do_update(
        index_elements=[products_table.c.product_id],
        set_={
            "category": statement.excluded.category,
            "sub_category": statement.excluded.sub_category,
            "product_name": statement.excluded.product_name,
        },
    )

    with engine.begin() as connection:
        connection.execute(statement)

    return len(products)


def main() -> None:
    from src.config.database import engine

    loaded_count = load_products_to_core(engine)
    print(f"Loaded {loaded_count} products into core.products.")


if __name__ == "__main__":
    main()
