import pandas as pd
import os


def extracte(DATASET_PATH) -> pd.DataFrame | None:
    if not os.path.exists(DATASET_PATH):
        return None
    try:
        df = pd.read_csv(DATASET_PATH, sep=",", encoding="latin-1")
    except pd.errors.EmptyDataError as e:
        raise ValueError(f"CSV file contains no data: {DATASET_PATH}") from e
    if df.empty:
        raise ValueError(f"CSV file is empty: {DATASET_PATH}")
    return df


def extracte_clean_dataset(DATASET_PATH) -> pd.DataFrame | None:
    if not os.path.exists(DATASET_PATH):
        return None
    try:
        df = pd.read_csv(DATASET_PATH, sep=",", encoding="utf-8")
    except pd.errors.EmptyDataError as e:
        raise ValueError(f"CSV file contains no data: {DATASET_PATH}") from e
    if df.empty:
        raise ValueError(f"CSV file is empty: {DATASET_PATH}")
    return df


def main():
    return extracte("data/raw/store_data.csv")


if __name__ == "__main__":
    df = main()
    if df.bool:
        print(df.head())
        print(df.shape)
        print(df.columns.tolist())
