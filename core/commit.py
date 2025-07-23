# core/commit.py

"""
Module pour la gestion des commits Git.
"""
import os
from typing import Optional, List
from .objects import Commit


class CommitManager:
    """Gestionnaire pour les objets commit Git."""
    
    def __init__(self, objects_dir: str):
        self.objects_dir = objects_dir
    
    def create_commit(self, tree_hash: str, message: str, author: str, parent_hash: str = None) -> str:
        """Crée un commit et retourne son hash."""
        commit = Commit(tree_hash, message, author, parent_hash)
        return commit.store()
    
    def get_commit(self, commit_hash: str) -> Commit:
        """Récupère un commit à partir de son hash."""
        return Commit.from_hash(commit_hash)
    
    def commit_exists(self, commit_hash: str) -> bool:
        """Vérifie si un commit existe."""
        path = f"{self.objects_dir}/commit/{commit_hash[:2]}/{commit_hash[2:]}"
        return os.path.exists(path)
    
    def get_commit_parent(self, commit_hash: str) -> Optional[str]:
        """Récupère le hash du commit parent."""
        commit = self.get_commit(commit_hash)
        return commit.parent_hash
    
    def get_commit_tree(self, commit_hash: str) -> str:
        """Récupère le hash du tree du commit."""
        commit = self.get_commit(commit_hash)
        return commit.tree_hash
    
    def get_commit_message(self, commit_hash: str) -> str:
        """Récupère le message du commit."""
        commit = self.get_commit(commit_hash)
        return commit.message
    
    def get_commit_author(self, commit_hash: str) -> str:
        """Récupère l'auteur du commit."""
        commit = self.get_commit(commit_hash)
        return commit.author