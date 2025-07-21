import os
import json
import hashlib

from functions.write_tree import write_tree

def add_file(file_path):
    if os.path.isdir(file_path):
        write_tree()
        if os.path.isdir(file_path):

            for root, dirs, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    add_file(file_path)

        return

    with open(file_path, "rb") as f:
        content = f.read()
    data_to_hash = file_path.encode() + b"\0" + content
    blob_hash = hashlib.sha1(data_to_hash).hexdigest()
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
            content = f.read().strip()
            if content:
                index = json.loads(content)
            else:
                index = {}
    else:
        index = {}

    rel_path = os.path.relpath(file_path, os.getcwd())
    file_stat = os.stat(file_path)

    index[rel_path] = blob_hash
    # Sauvegarder l'index
    with open(index_path, "w") as f:
        json.dump(index, f)


def status_all():
    index_path = ".fyt/index"
    project_root = os.path.join(os.getcwd(), "projet-test")

    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            content = f.read().strip()
            if content:
                index = json.loads(content)
            else:
                index = {}
    else:
        index = {}

    tracked_files = set(index.keys())
    working_dir_files = set()

    for root, dirs, files in os.walk(project_root):
        # Exclure les dossiers cachés et __pycache__
        rel_root = os.path.relpath(root, project_root)
        if rel_root == ".fyt" or rel_root.startswith(".fyt" + os.sep):
            continue
        if rel_root.startswith(".git") or rel_root.startswith("__pycache__") or rel_root.startswith("Objects" + os.sep + "__pycache__"):
            continue
        # Exclure tous les dossiers cachés
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.startswith('.') or file.endswith('.pyc'):
                continue
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, os.getcwd())  # rel_path par rapport à la racine du projet global
            working_dir_files.add(rel_path)

            with open(path, "rb") as f:
                content = f.read()
            current_hash = hashlib.sha1(content).hexdigest()

            if rel_path not in index:
                print(f"{rel_path}: nouveau fichier non suivi")
            elif index[rel_path] != current_hash:
                print(f"{rel_path}: modifié")
            else:
                print(f"{rel_path}: inchangé")

    for tracked in tracked_files - working_dir_files:
        print(f"{tracked}: supprimé")