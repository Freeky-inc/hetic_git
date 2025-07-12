import os
import json
import hashlib

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Fichier '{file_path}' supprimé.")
    else:
        print(f"Fichier '{file_path}' introuvable.")
