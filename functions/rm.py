import os
import json

def remove_from_index(file_path, index_dir=".git"):
    index_path = os.path.join(index_dir, "index")

    if not os.path.exists(index_path):
        return

    try:
        with open(index_path, "r") as f:
            index = json.load(f)
    except json.JSONDecodeError:
        index = {}

    rel_path = os.path.relpath(file_path, os.getcwd())

    if rel_path in index:
        del index[rel_path]
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)

def fyt_rm(file_path, index_dir=".git"):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} supprimé du disque.")
    else:
        print(f"Fichier introuvable : {file_path}")
        return

    # Supprime le fichier de l'index
    remove_from_index(file_path, index_dir)
    print(f"{file_path} supprimé de l'index.")
