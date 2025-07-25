import os
import json
import hashlib

from functions.write_tree import write_tree

def find_project_root(start_path):
    """Remonte les dossiers jusqu'à trouver le dossier contenant .fyt"""
    current = os.path.abspath(start_path)
    while True:
        if os.path.isdir(os.path.join(current, ".fyt")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise FileNotFoundError("Impossible de trouver le dossier racine du projet (.fyt)")
        current = parent


def add_file(file_path):
    project_root = find_project_root(file_path)
    fyt_dir = os.path.join(project_root, ".fyt")
    blob_dir = os.path.join(fyt_dir, "objects", "blob")
    index_path = os.path.join(fyt_dir, "index")

    if os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            dirs[:] = [d for d in dirs if d != '.fyt' and not d.startswith('.') and d != '__pycache__']
            for file in files:
                full_path = os.path.join(root, file)
                if ".fyt" in os.path.relpath(full_path, file_path).split(os.sep):
                    continue
                add_file(full_path)
        return

    with open(file_path, "rb") as f:
        content = f.read()
    # Chemin relatif à la racine du projet
    rel_path = os.path.relpath(os.path.abspath(file_path), project_root)
    data_to_hash = rel_path.encode() + b"\0" + content
    blob_hash = hashlib.sha1(data_to_hash).hexdigest()
    os.makedirs(blob_dir, exist_ok=True)
    blob_path = os.path.join(blob_dir, blob_hash)

    with open(blob_path, "wb") as f:
        f.write(content)

    print(f"Fichier '{rel_path}' ajouté (Blob: {blob_hash})")
    update_index(file_path, blob_hash)
    print(f"Fichier '{rel_path}' ajouté (Blob: {blob_hash})")

        
def update_index(file_path, blob_hash):
    index_path = "projet-test/.fyt/index"
    # Exclure les fichiers dans le dossier .fyt
    if ".fyt" in os.path.relpath(file_path, "projet-test").split(os.sep):
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        index = json.loads(content) if content else {}
    
    # Chemin relatif à la racine du projet
    rel_path = os.path.relpath(file_path, os.getcwd())
    index[rel_path] = blob_hash

    # Sauvegarder l'index mis à jour
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def status_all():
    index_path = "projet-test/.fyt/index"
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
        
        else:
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