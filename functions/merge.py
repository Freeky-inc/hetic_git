import argparse
import os
import json
import hashlib
import datetime

# Récupère le hash du dernier commit d’une branche donnée.

def get_branch_commit(branch):
    ref_path = os.path.join("projet-test", ".fyt", "refs", "heads", branch)
    if not os.path.exists(ref_path):
        print(f"Branche {branch} introuvable.")
        return None
    with open(ref_path, "r") as f:
        return f.read().strip()

# Récupère le(s) parent(s) d’un commit.

def get_commit_parents(commit_sha):
    commit_path = os.path.join("projet-test", ".fyt", "objects", "commit", commit_sha)
    if not os.path.exists(commit_path):
        return []
    with open(commit_path, "rb") as f:
        data = json.load(f)
    parents = data.get("parents", [])
    return parents if parents else []

# Récupère tous les ancêtres d’un commit (pour trouver un ancêtre commun lors d’un merge).

def get_ancestors(commit_sha):
    ancestors = set()
    stack = [commit_sha]
    while stack:
        sha = stack.pop()
        if sha and sha not in ancestors:
            ancestors.add(sha)
            stack.extend(get_commit_parents(sha))
    return ancestors

# Trouve l’ancêtre commun le plus proche entre deux commits (base du merge).

def find_common_ancestor(sha1, sha2):
    ancestors1 = get_ancestors(sha1)
    stack = [sha2]
    while stack:
        sha = stack.pop()
        if sha in ancestors1:
            return sha
        stack.extend(get_commit_parents(sha))
    return None

# Effectue la fusion entre deux branches.

def merge(branch1, branch2):
    sha1 = get_branch_commit(branch1)
    sha2 = get_branch_commit(branch2)
    if not sha1 or not sha2:
        print("Impossible de trouver les commits des branches.")
        return

    ancestor = find_common_ancestor(sha1, sha2)
    if not ancestor:
        print("Aucun ancêtre commun trouvé.")
        return

    # Charger les trees des deux commits
    def get_tree(sha):
        path = os.path.join("projet-test", ".fyt", "objects", "commit", sha)
        with open(path, "rb") as f:
            data = json.load(f)
        return data["tree"]

    tree1 = get_tree(sha1)
    tree2 = get_tree(sha2)

    # Fusion simplifiée : on prend tous les fichiers des deux trees (sans gestion de conflit)
    tree1_path = os.path.join("projet-test", ".fyt", "objects", "tree", tree1)
    tree2_path = os.path.join("projet-test", ".fyt", "objects", "tree", tree2)
    with open(tree1_path, "rb") as f:
        files1 = dict(json.load(f)["files"])
    with open(tree2_path, "rb") as f:
        files2 = dict(json.load(f)["files"])

    merged_files = {}
    all_files = set(files1.keys()) | set(files2.keys())
    for file_path in all_files:
        blob1 = files1.get(file_path)
        blob2 = files2.get(file_path)
        if blob1 and blob2:
            # Les deux branches ont le fichier, vérifier le contenu
            blob1_path = os.path.join("projet-test", ".fyt", "objects", "blob", blob1)
            blob2_path = os.path.join("projet-test", ".fyt", "objects", "blob", blob2)
            with open(blob1_path, "rb") as f1, open(blob2_path, "rb") as f2:
                content1 = f1.read()
                content2 = f2.read()
            if content1 != content2:
                # Conflit, créer un nouveau blob avec les marqueurs
                conflict_content = (
                    f"<<<<<<< {branch1}\n".encode() +
                    content1 +
                    b"\n=======\n" +
                    content2 +
                    f"\n>>>>>>> {branch2}\n".encode()
                )
                conflict_blob_hash = hashlib.sha1(conflict_content).hexdigest()
                conflict_blob_path = os.path.join("projet-test", ".fyt", "objects", "blob", conflict_blob_hash)
                with open(conflict_blob_path, "wb") as f:
                    f.write(conflict_content)
                merged_files[file_path] = conflict_blob_hash
            else:
                merged_files[file_path] = blob1  # Pas de conflit, contenu identique
        elif blob1:
            merged_files[file_path] = blob1
        elif blob2:
            merged_files[file_path] = blob2

    merged_tree_data = {"files": list(merged_files.items())}
    merged_tree_json = json.dumps(merged_tree_data).encode()
    merged_tree_hash = hashlib.sha1(merged_tree_json).hexdigest()

    os.makedirs(".fyt/objects/tree", exist_ok=True)
    with open(f".fyt/objects/tree/{merged_tree_hash}", "wb") as f:
        f.write(merged_tree_json)

    # Créer le commit de merge
    commit_data = {
        "tree": merged_tree_hash,
        "message": f"Merge {branch1} into {branch2}",
        "date": datetime.datetime.now().isoformat(),
        "parents": [sha1, sha2]
    }
    commit_json = json.dumps(commit_data).encode()
    commit_hash = hashlib.sha1(commit_json).hexdigest()

    os.makedirs(os.path.join("projet-test", ".fyt", "objects", "commit"), exist_ok=True)
    with open(os.path.join("projet-test", ".fyt", "objects", "commit", commit_hash), "wb") as f:
        f.write(commit_json)

    # Mettre à jour la branche cible (branch1)
    ref_path = os.path.join("projet-test", ".fyt", "refs", "heads", branch1)
    with open(ref_path, "w") as f:
        f.write(commit_hash)

    print(f"Merge terminé. Nouveau commit de merge : {commit_hash[:6]}")