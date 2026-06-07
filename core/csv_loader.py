import pandas as pd


ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "cp1252",
    "ISO-8859-1",
    "latin1"
]


def read_csv_safe(file_path):
    for enc in ENCODINGS:
        try:
            return pd.read_csv(
                file_path,
                encoding=enc,
                on_bad_lines='skip'
            )
        except:
            continue

    # last fallback
    return pd.read_csv(file_path, encoding="latin1", errors="replace")