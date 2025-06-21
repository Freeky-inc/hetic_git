# commands/add.py
"""
# commands/add.py
Module pour ajouter un fichier à l'index Git.
Ce module lit un fichier, crée un objet Blob, le stocke et l'ajoute à l'index.
"""
from core.objects import Blob
from core.index import GitIndex

def run(filename):
    with open(filename, "rb") as f:
        data = f.read()

    blob = Blob(data)
    sha = blob.store()

    index = GitIndex()
    index.add(filename, sha)

    print(f"Added {filename} to index as blob {sha}")


# import hashlib

# def add_file(file_path):
#     with open(file_path, "rb") as f:
#         content = f.read()
#     blob_hash = hashlib.sha1(content).hexdigest()
#     blob_path = f".fyt/objects/{blob_hash}"

#     with open(blob_path, "wb") as f:
#         f.write(content)
#     print(f"Fichier '{file_path}' ajouté (Blob: {blob_hash})")
