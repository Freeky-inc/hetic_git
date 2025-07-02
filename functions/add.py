import os
import json
import hashlib

def add_file(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    blob_hash = hashlib.sha1(content).hexdigest()
    blob_dir = ".fyt/objects/blob"
    os.makedirs(blob_dir, exist_ok=True)
    blob_path = os.path.join(blob_dir, blob_hash)

    with open(blob_path, "wb") as f:
        f.write(content)

    update_index(file_path, blob_hash)
    print(f"Fichier '{file_path}' ajouté (Blob: {blob_hash})")

def update_index(file_path, blob_hash):

    index_path = ".fyt/index"
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            index = json.load(f)
    else:
        index = {}

    rel_path = os.path.relpath(file_path, os.getcwd())
    file_stat = os.stat(file_path)

    index[rel_path] = blob_hash
    # Sauvegarder l'index
    with open(index_path, "w") as f:
        json.dump(index, f)