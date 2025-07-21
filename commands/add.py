# commands/add.py
"""
# commands/add.py
Module pour ajouter un ou plusieurs fichiers à l'index Git.
Ce module lit le(s) fichier(s), crée un objet Blob, le stocke et l'ajoute à l'index.
Il peut également ajouter un dossier et tous ses fichiers récursivement.
"""
from core.objects import Blob
from core.index import GitIndex

def run(filenames):
    for filename in filenames:
        with open(filename, "rb") as f:
            data = f.read()

        blob = Blob(data)
        sha = blob.store()

        index = GitIndex()
        index.add(filename, sha)

        print(f"Added {filename} to index as blob {sha}")

