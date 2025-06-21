# core/refs.py

"""
# core/refs.py
Module pour la gestion des références Git (HEAD, branches).
Il permet de lire et d'écrire des références dans le dépôt Git.
"""
import os

def get_head():
    with open(".git/HEAD") as f:
        return f.read().strip().split(" ")[1]

def update_ref(ref, sha):
    with open(f".git/{ref}", "w") as f:
        f.write(sha)

def read_ref(ref):
    path = f".git/{ref}"
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return None
