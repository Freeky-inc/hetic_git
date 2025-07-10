import os
import json
import hashlib
import datetime

def commit_changes(message):
    index_path = ".fyt/index"
    if not os.path.exists(index_path):
        print("Rien à commit. Utilisez 'add' avant.")
        return

    # Charger l'index
    with open(index_path, "r") as f:
        index = json.load(f)
    # Créer un Tree (simplifié)
    tree_data = {"files": list(index.items())}  # En vrai, on stocke une structure de dossiers/fichiers
    tree_json = json.dumps(tree_data).encode()
    tree_hash = hashlib.sha1(tree_json).hexdigest()

    os.makedirs(".fyt/objects/tree", exist_ok=True)

    with open(f".fyt/objects/tree/{tree_hash}", "wb") as f:
        f.write(tree_json)

    # Créer un Commit
    commit_data = {
        "tree": tree_hash,
        "message": message,
        "date": datetime.datetime.now().isoformat(),
    }
    commit_json = json.dumps(commit_data).encode()
    commit_hash = hashlib.sha1(commit_json).hexdigest()

    os.makedirs(".fyt/objects/commit", exist_ok=True)

    with open(f".fyt/objects/commit/{commit_hash}", "wb") as f:
        f.write(commit_json)

    # Mettre à jour la référence (branche)
    with open(".fyt/refs/heads/main", "w") as f:
        f.write(commit_hash)

    print(f"Commit [{commit_hash[:6]}]: {message}")

    # git status