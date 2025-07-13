import os
import json
import hashlib

def remove_from_index(file_path):
    index_path = ".fyt/index"

    if not os.path.exists(index_path):
        return
    with open(index_path, "r") as f:
        index = json.load(f)
    rel_path = os.path.relpath(file_path, os.getcwd())
    if rel_path in index:
        del index[rel_path]  # Supprimer le fichier de l'index

        with open(index_path, "w") as f:
            json.dump(index, f)

def fyt_rm(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        remove_from_index(file_path)
        print(f"Removed '{file_path}' from working directory and index.")
    else:
        print(f"File '{file_path}' does not exist.")