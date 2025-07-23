 # core/repository.py

"""
Module pour la gestion du dépôt Git.
Ce module fournit une classe Repository qui centralise l'accès à tous les composants
du dépôt Git (objets, index, références, etc.).
"""
import os
from typing import Optional, List
from pathlib import Path

from .objects import Blob, Tree, Commit, TreeEntry
from .index import GitIndex
from .refs import GitRefs
from .blob import BlobManager
from .tree import TreeManager
from .commit import CommitManager


class Repository:
    """Représente un dépôt Git et centralise toutes les opérations."""
    
    def __init__(self, path: str = "."):
        self.path = Path(path).resolve()
        self.git_dir = self.path / ".fyt"
        self.index = GitIndex(str(self.git_dir / "index"))
        self.refs = GitRefs(str(self.git_dir))
        self.blob_manager = BlobManager(str(self.git_dir / "objects"))
        self.tree_manager = TreeManager(str(self.git_dir / "objects"))
        self.commit_manager = CommitManager(str(self.git_dir / "objects"))

    def is_git_repository(self) -> bool:
        """Vérifie si le répertoire est un dépôt Git valide."""
        return self.git_dir.exists() and (self.git_dir / "HEAD").exists()

    def init(self) -> bool:
        """Initialise un nouveau dépôt Git."""
        try:
            # Créer la structure de base
            (self.git_dir / "objects").mkdir(parents=True, exist_ok=True)
            (self.git_dir / "refs" / "heads").mkdir(parents=True, exist_ok=True)
            (self.git_dir / "refs" / "tags").mkdir(parents=True, exist_ok=True)
            
            # Créer HEAD initial
            self.refs.set_head("refs/heads/main", symbolic=True)
            
            # Créer un commit initial vide
            empty_tree = Tree([])
            tree_hash = empty_tree.store()
            
            initial_commit = Commit(
                tree_hash=tree_hash,
                message="Initial commit",
                author="Git User <user@example.com>"
            )
            commit_hash = initial_commit.store()
            
            # Pointer main vers le commit initial
            self.refs.write_ref("heads/main", commit_hash)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'initialisation du dépôt: {e}")
            return False

    def add_file(self, filepath: str) -> Optional[str]:
        """Ajoute un fichier au dépôt et retourne son hash."""
        try:
            full_path = self.path / filepath
            
            if not full_path.exists():
                print(f"Fichier non trouvé: {filepath}")
                return None
            
            if not full_path.is_file():
                print(f"Le chemin n'est pas un fichier: {filepath}")
                return None
            
            # Créer le blob
            blob = Blob.from_file(str(full_path))
            blob_hash = blob.store()
            
            # Ajouter à l'index
            self.index.add(filepath, blob_hash)
            
            return blob_hash
        except Exception as e:
            print(f"Erreur lors de l'ajout du fichier {filepath}: {e}")
            return None

    def add_files(self, filepaths: List[str]) -> List[str]:
        """Ajoute plusieurs fichiers au dépôt."""
        hashes = []
        for filepath in filepaths:
            blob_hash = self.add_file(filepath)
            if blob_hash:
                hashes.append(blob_hash)
        return hashes

    def create_commit(self, message: str, author: str = None) -> Optional[str]:
        """Crée un nouveau commit avec les fichiers staged."""
        try:
            if not author:
                author = "Git User <user@example.com>"
            
            # Récupérer les fichiers staged
            staged_files = self.index.get_all_files()
            
            if not staged_files:
                print("Aucun fichier à commiter.")
                return None
            
            # Créer les entrées du tree
            tree_entries = []
            for filename in staged_files:
                entry = self.index.get_entry(filename)
                if entry:
                    # Stocker explicitement le blob pour ce fichier
                    full_path = self.path / filename
                    blob = Blob.from_file(str(full_path))
                    blob_hash = blob.store("blob")  # Storage happens here
                    tree_entry = TreeEntry(
                        mode=entry.mode,
                        name=filename,
                        sha=blob_hash  # Use the hash of the stored blob
                    )
                    tree_entries.append(tree_entry)
            
            # Créer le tree
            tree = Tree(tree_entries)
            tree_hash = tree.store()
            
            # Créer le commit
            commit = Commit(
                tree_hash=tree_hash,
                message=message,
                author=author
            )
            commit_hash = commit.store()
            
            # Mettre à jour HEAD
            self.refs.write_ref("heads/main", commit_hash)
            
            # Vider l'index
            self.index.clear()
            
            return commit_hash
        except Exception as e:
            print(f"Erreur lors de la création du commit: {e}")
            return None

    def get_status(self) -> dict:
        """Retourne le statut du dépôt."""
        status = {
            "staged": [],
            "modified": [],
            "untracked": []
        }
        
        # Fichiers staged
        staged_files = self.index.get_all_files()
        for filename in staged_files:
            status["staged"].append(filename)
        
        return status

    def get_log(self, max_entries: int = 10) -> List[dict]:
        """Retourne l'historique des commits."""
        commits = []
        current_hash = self.refs.get_head()
        
        while current_hash and len(commits) < max_entries:
            try:
                commit = Commit.from_hash(current_hash)
                commits.append({
                    "hash": current_hash,
                    "message": commit.message,
                    "author": commit.author,
                    "date": commit.timestamp
                })
                current_hash = commit.parent_hash
            except Exception:
                break
        
        return commits

    def checkout_file(self, filepath: str, commit_hash: str = None) -> bool:
        """Restaure un fichier depuis un commit."""
        try:
            if not commit_hash:
                commit_hash = self.refs.get_head()
            
            commit = Commit.from_hash(commit_hash)
            tree = Tree.from_hash(commit.tree_hash)
            
            # Trouver le fichier dans le tree
            entry = tree.find_entry(filepath)
            if not entry:
                print(f"Fichier {filepath} non trouvé dans le commit {commit_hash}")
                return False
            
            # Restaurer le fichier
            blob = Blob.from_hash(entry.sha)
            with open(filepath, 'wb') as f:
                f.write(blob.content)
            
            return True
        except Exception as e:
            print(f"Erreur lors du checkout du fichier {filepath}: {e}")
            return False

    def get_file_content(self, filepath: str, commit_hash: str = None) -> Optional[bytes]:
        """Récupère le contenu d'un fichier depuis un commit."""
        try:
            if not commit_hash:
                commit_hash = self.refs.get_head()
            
            commit = Commit.from_hash(commit_hash)
            tree = Tree.from_hash(commit.tree_hash)
            
            entry = tree.find_entry(filepath)
            if not entry:
                return None
            
            blob = Blob.from_hash(entry.sha)
            return blob.content
        except Exception:
            return None

    def __repr__(self) -> str:
        return f"Repository(path={self.path}, git_dir={self.git_dir})"