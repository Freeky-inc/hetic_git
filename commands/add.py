# commands/add.py
"""
Module pour ajouter un ou plusieurs fichiers à l'index Git via le service add_services.
"""
from services.add_services import add

def run(filenames):
    results = add(filenames)
    for file, blob_hash in results:
        if blob_hash:
            print(f"Ajouté: {file} (blob {blob_hash})")
        else:
            print(f"Erreur lors de l'ajout de {file}")