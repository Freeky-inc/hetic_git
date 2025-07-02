import json
import os

def show_ref():
    index_path = ".fyt/index"
    if not os.path.exists(index_path):
        print("Aucune référence trouvée.")
        return
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    for ref, hash_value in index.items():
        print(f"{ref}: {hash_value}")