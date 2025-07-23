# core/__init__.py

"""
Module core pour le système de gestion de version Git.
Ce module exporte les classes principales utilisées par les autres modules.
"""

from .repository import Repository
from .objects import Blob, Tree, Commit, TreeEntry
from .index import GitIndex
from .refs import GitRefs
from .blob import BlobManager
from .tree import TreeManager
from .commit import CommitManager

__all__ = [
    'Repository',
    'Blob',
    'Tree', 
    'Commit',
    'TreeEntry',
    'GitIndex',
    'GitRefs',
    'BlobManager',
    'TreeManager',
    'CommitManager'
] 