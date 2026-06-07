import os


def normalize_customer_id(user_input: str) -> str:
    digits = ''.join(filter(str.isdigit, user_input))
    return f"ID{digits.zfill(10)}"


def find_customer_recursive(root_folder: str, customer_id: str):

    target_id = normalize_customer_id(customer_id)
    results = []

    def walk(current_path, current_ub3=None, ub3_path=None):

        try:
            items = os.listdir(current_path)
        except:
            return

        for item in items:
            full_path = os.path.join(current_path, item)

            if not os.path.isdir(full_path):
                continue

            # Detect UB3 folder (top-level or nested)
            if item.startswith("UB"):
                current_ub3 = item
                ub3_path = full_path

            # Detect customer ID folder
            if item == target_id:

                csv_files = [
                    os.path.join(full_path, f)
                    for f in os.listdir(full_path)
                    if f.endswith(".csv")
                ]

                results.append({
                    "ub3_folder": current_ub3,
                    "ub3_path": ub3_path,
                    "customer_id": item,
                    "id_path": full_path,
                    "csv_files": csv_files
                })

            # Continue recursion
            walk(full_path, current_ub3, ub3_path)

    walk(root_folder)

    return results