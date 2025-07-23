import os
import json
import hashlib

def sha1_file(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()

def load_index(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read().strip()
            print('si fichier vide retourne un dictionnaire vide')
            return json.loads(content) if content else {}
    return {}

def status_all():
    index_path = ".fyt/index" # les fichiers
    staging_path = ".fyt/staging"
    project_root = os.path.join(os.getcwd(), "projet-test")

    index = load_index(index_path)
    staging = load_index(staging_path)

    tracked_files = set(index.keys())
    staged_files = set(staging.keys())
    working_dir_files = set()

    changes_to_be_committed = []
    changes_not_staged = []
    untracked_files = []
    deleted_files = []

    for root, dirs, files in os.walk(project_root):
        rel_root = os.path.relpath(root, project_root)

        if rel_root.startswith(".fyt") or rel_root.startswith(".git") or rel_root.startswith("__pycache__"):
            continue

        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.startswith('.') or file.endswith('.pyc'):
                continue

            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, os.getcwd())

            working_dir_files.add(rel_path)
            current_hash = sha1_file(path)

            # Fichier non suivi
            if rel_path not in index and rel_path not in staging:
                untracked_files.append(rel_path)

            # Fichier modifié et staged
            elif rel_path in staging:
                if rel_path not in index:
                    changes_to_be_committed.append((rel_path, "new file"))
                elif staging[rel_path] != index[rel_path]:
                    changes_to_be_committed.append((rel_path, "modified"))

            # Fichier modifié mais pas staged
            elif rel_path in index and current_hash != index[rel_path]:
                changes_not_staged.append(rel_path)

    # Fichiers supprimés
    for tracked in tracked_files:
        if tracked not in working_dir_files:
            if tracked in staging:
                changes_to_be_committed.append((tracked, "deleted"))
            else:
                deleted_files.append(tracked)

    # Affichage
    if changes_to_be_committed:
        print("Changes to be committed:")
        print("  (use \"fyt reset <file>\" to unstage)")
        for file, status in changes_to_be_committed:
            print(f"    {status}:   {file}")
        print()

    #Cette partie la permet
    if changes_not_staged or deleted_files:
        print("Changes not staged for commit:")
        print("  (use \"fyt add <file>\" to update what will be committed)")
        for file in changes_not_staged:
            print(f"    modified:   {file}")
        for file in deleted_files:
            print(f"    deleted:    {file}")
        print()

    if untracked_files:
        print("Untracked files:")
        print("  (use \"fyt add <file>\" to include in what will be committed)")
        for file in untracked_files:
            print(f"    {file}")
        print()

    if not (changes_to_be_committed or changes_not_staged or deleted_files or untracked_files):
        print("nothing to commit, working tree clean")
