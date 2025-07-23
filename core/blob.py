# core/blob.py

"""
Module pour la gestion des blobs Git.
"""
import os
from .objects import Blob


class BlobManager:
    """Gestionnaire pour les objets blob Git."""
    
    def __init__(self, objects_dir: str):
        self.objects_dir = objects_dir
    
    def create_blob(self, filepath: str) -> str:
        """Crée un blob à partir d'un fichier et retourne son hash."""
        blob = Blob.from_file(filepath)
        return blob.store()
    
    def get_blob(self, blob_hash: str) -> Blob:
        """Récupère un blob à partir de son hash."""
        return Blob.from_hash(blob_hash)
    
    def blob_exists(self, blob_hash: str) -> bool:
        """Vérifie si un blob existe."""
        path = f"{self.objects_dir}/blob/{blob_hash[:2]}/{blob_hash[2:]}"
        return os.path.exists(path)