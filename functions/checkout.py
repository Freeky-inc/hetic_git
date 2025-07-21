import os
import json
import sys

def checkout(b, branch_or_sha):
    # Vérifier le dépôt
    if not os.path.exists('.fyt'):
        print("Aucun dépôt Fyt trouvé.")
        return

    ref = branch_or_sha
    # Création d'une nouvelle branche si l'argument -b est présent
    if b:
        with open('.fyt/HEAD', 'r') as f:
            current_ref = f.read().strip()
        if current_ref.startswith('ref:'):
            current_ref = current_ref.split(' ')[1]
            current_commit_file = os.path.join('.fyt', current_ref)
            with open(current_commit_file, 'r') as f:
                current_commit_sha = f.readlines()[-1].split()[0]
        else:
            current_commit_sha = current_ref
        # Créer la branche
        ref_path = os.path.join('.fyt', 'refs', 'heads', ref)
        with open(ref_path, 'w') as f:
            f.write(current_commit_sha)
        print(f"Branche '{ref}' créée sur {current_commit_sha}.")
        # HEAD sur la nouvelle branche
        with open('.fyt/HEAD', 'w') as f:
            f.write(f"ref: refs/heads/{ref}")
        commit_sha = current_commit_sha
    else:
        # Changement de branche ou commit
        ref_path = os.path.join('.fyt', 'refs', 'heads', ref)
        if os.path.exists(ref_path):
            with open(ref_path, 'r') as f:
                commit_sha = f.read().strip()
            with open('.fyt/HEAD', 'w') as f:
                f.write(f"ref: refs/heads/{ref}")
        else:
            commit_sha = ref
            with open('.fyt/HEAD', 'w') as f:
                f.write(commit_sha)

    # Charger le commit
    commit_path = os.path.join('.fyt', 'commits', commit_sha)
    if not os.path.exists(commit_path):
        print(f"Commit {commit_sha} introuvable.")
        return
    with open(commit_path, 'r') as f:
        commit_data = json.load(f)

    # Restaurer les fichiers du commit avec gestion des conflits
    for file_path, blob_sha in commit_data.items():
        blob_path = os.path.join('.fyt', 'objects', 'blob', blob_sha)
        if not os.path.exists(blob_path):
            print(f"Blob {blob_sha} manquant pour {file_path}.")
            continue
        # Vérifier les conflits
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                current_content = f.read()
            with open(blob_path, 'rb') as f:
                new_content = f.read()
            if current_content != new_content:
                print(f"Conflit: {file_path} modifié localement. Non écrasé.")
                continue
        # Créer les dossiers si besoin
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(blob_path, 'rb') as blob_file:
            content = blob_file.read()
        with open(file_path, 'wb') as out_file:
            out_file.write(content)
    print(f"Checkout terminé sur {branch_or_sha}.")
