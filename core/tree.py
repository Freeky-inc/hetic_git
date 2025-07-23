# core/tree.py

"""
Module pour la gestion des trees Git.
"""
import os
from typing import List, Dict, Optional
from .objects import Tree, TreeEntry


class TreeManager:
    """Gestionnaire pour les objets tree Git."""
    
    def __init__(self, objects_dir: str):
        self.objects_dir = objects_dir
    
    def create_tree(self, entries: List[TreeEntry]) -> str:
        """Crée un tree à partir d'une liste d'entrées et retourne son hash."""
        tree = Tree.from_entries(entries)
        return tree.store()
    
    def get_tree(self, tree_hash: str) -> Tree:
        """Récupère un tree à partir de son hash."""
        return Tree.from_hash(tree_hash)
    
    def tree_exists(self, tree_hash: str) -> bool:
        """Vérifie si un tree existe."""
        path = f"{self.objects_dir}/tree/{tree_hash[:2]}/{tree_hash[2:]}"
        return os.path.exists(path)
    
    def build_tree_from_directory(self, directory_path: str, base_path: str = "") -> Optional[str]:
        """Construit un tree à partir d'un répertoire."""
        entries = []
        
        try:
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                rel_path = os.path.join(base_path, item) if base_path else item
                
                if os.path.isfile(item_path):
                    # Créer un blob pour le fichier
                    from .blob import BlobManager
                    blob_manager = BlobManager(self.objects_dir)
                    blob_hash = blob_manager.create_blob(item_path)
                    
                    # Déterminer le mode (simplifié)
                    mode = "100644"  # Fichier normal
                    if os.access(item_path, os.X_OK):
                        mode = "100755"  # Fichier exécutable
                    
                    entry = TreeEntry(mode=mode, name=item, sha=blob_hash)
                    entries.append(entry)
                
                elif os.path.isdir(item_path) and not item.startswith('.'):
                    # Récursion pour les sous-répertoires
                    sub_tree_hash = self.build_tree_from_directory(item_path, rel_path)
                    if sub_tree_hash:
                        entry = TreeEntry(mode="040000", name=item, sha=sub_tree_hash)
                        entries.append(entry)
            
            if entries:
                return self.create_tree(entries)
            return None
            
        except Exception as e:
            print(f"Erreur lors de la construction du tree: {e}")
            return None 