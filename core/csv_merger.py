import os
import pandas as pd

from core.csv_loader import read_csv_safe
from core.schema import EXPECTED_COLUMNS
# from core.data_cleaner import clean_dataframe
from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from core.data_cleaner import clean_value


def merge_customer_data(customer_results):

    all_data = []

    stats = {
        "merged_files": 0,
        "skipped_unlock": 0,
        "failed_files": 0,
        "errors": []
    }

    for customer in customer_results:

        ub3 = customer["ub3_folder"]
        customer_id = customer["customer_id"]

        for file_path in customer["csv_files"]:

            filename = os.path.basename(
                file_path
            ).upper()

            if filename.startswith(
                "UNLOCK"
            ):
                stats["skipped_unlock"] += 1
                continue

            try:
                df = read_csv_safe(file_path)

                # Ensure all columns exist
                for col in EXPECTED_COLUMNS:
                    if col not in df.columns:
                        df[col] = None

                df = df[EXPECTED_COLUMNS]

                # Add metadata (VERY IMPORTANT for fraud tracking)
                df["UB3"] = ub3
                df["CustomerID"] = customer_id
                df["SourceFile"] = os.path.basename(file_path)

                all_data.append(df)
                stats["merged_files"] += 1

            except Exception as e:

                stats["failed_files"] += 1

                stats["errors"].append(
                    f"{os.path.basename(file_path)} : {str(e)}"
                )

    if not all_data:
        return None, stats

    merged_df = pd.concat(all_data, ignore_index=True)
    return merged_df, stats


def export_excel(df, output_path):

    wb = Workbook()
    ws = wb.active

    # Write header
    ws.append(list(df.columns))

    for row_idx, row in enumerate(df.itertuples(index=False), start=2):

        cleaned_row = []

        for col_idx, value in enumerate(row):

            try:
                cleaned_value = clean_value(value)
                cleaned_row.append(cleaned_value)

            except Exception as e:
                print(
                    f"Clean Error -> Row:{row_idx} "
                    f"Col:{df.columns[col_idx]} "
                    f"Value:{repr(value)}"
                )
                raise

        try:
            ws.append(cleaned_row)

        except IllegalCharacterError:

            print("\n=== BAD DATA FOUND ===")
            print(f"Row Number: {row_idx}")

            for col_name, value in zip(df.columns, cleaned_row):
                print(
                    f"{col_name}: {repr(value)}"
                )

            raise
    wb.save(output_path)
