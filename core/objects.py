 # core/objects.py

"""
Module pour les objets Git de base.
Ce module définit les classes de base pour tous les objets Git (blob, tree, commit).
"""
import os
import zlib
import hashlib
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TreeEntry:
    """Représente une entrée dans un tree Git."""
    mode: str
    name: str
    sha: str


class GitObject:
    """Classe de base pour tous les objets Git."""
    
    def __init__(self, content: bytes):
        self.content = content
        self.type = "object"  # Sera redéfini par les sous-classes
    
    def serialize(self) -> bytes:
        """Sérialise l'objet pour le stockage."""
        raise NotImplementedError
    
    def compute_hash(self) -> str:
        """Calcule le hash SHA1 de l'objet."""
        return hashlib.sha1(self.serialize()).hexdigest()
    
    def store(self, type_: str = None) -> str:
        """Stocke l'objet dans le dépôt Git et retourne son hash."""
        sha = self.compute_hash()
        # Utiliser le type de l'objet si aucun type n'est fourni
        if type_ is None:
            type_ = self.type
        path = f".fyt/objects/{type_}/{sha[:2]}/{sha[2:]}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "wb") as f:
            f.write(zlib.compress(self.serialize()))
        return sha


class Blob(GitObject):
    """Représente un objet blob Git (contenu de fichier)."""
    
    def __init__(self, content: bytes):
        super().__init__(content)
        self.type = "blob"
    
    def serialize(self) -> bytes:
        """Sérialise le blob."""
        return self.content
    
    @classmethod
    def from_file(cls, filepath: str) -> 'Blob':
        """Crée un blob à partir d'un fichier."""
        with open(filepath, 'rb') as f:
            content = f.read()
        return cls(content)
    
    @classmethod
    def from_hash(cls, blob_hash: str) -> 'Blob':
        """Crée un blob à partir de son hash."""
        # Lire depuis le stockage
        path = f".fyt/objects/blob/{blob_hash[:2]}/{blob_hash[2:]}"
        with open(path, 'rb') as f:
            compressed_data = f.read()
        content = zlib.decompress(compressed_data)
        return cls(content)
    
    def hash(self) -> str:
        """Calcule le hash du blob sans le stocker."""
        return self.compute_hash()


class Tree(GitObject):
    """Représente un objet tree Git (répertoire)."""
    
    def __init__(self, entries: List[TreeEntry]):
        self.entries = sorted(entries, key=lambda e: e.name)
        super().__init__(b"")  # Le contenu sera calculé lors de la sérialisation
        self.type = "tree"
    
    def serialize(self) -> bytes:
        """Sérialise le tree."""
        data = b""
        for entry in self.entries:
            # Format: mode name\0sha
            entry_data = f"{entry.mode} {entry.name}".encode('utf-8') + b'\0'
            entry_data += bytes.fromhex(entry.sha)
            data += entry_data
        return data
    
    @classmethod
    def from_entries(cls, entries: List[TreeEntry]) -> 'Tree':
        """Crée un tree à partir d'une liste d'entrées."""
        return cls(entries)
    
    @classmethod
    def from_hash(cls, tree_hash: str) -> 'Tree':
        """Crée un tree à partir de son hash."""
        # Lire depuis le stockage
        path = f".fyt/objects/tree/{tree_hash[:2]}/{tree_hash[2:]}"
        with open(path, 'rb') as f:
            compressed_data = f.read()
        content = zlib.decompress(compressed_data)
        
        # Parser le contenu
        entries = []
        pos = 0
        while pos < len(content):
            # Trouver la fin du mode et du nom
            null_pos = content.find(b'\0', pos)
            if null_pos == -1:
                break
            
            # Extraire le mode et le nom
            mode_name = content[pos:null_pos].decode('utf-8')
            space_pos = mode_name.find(' ')
            
            if space_pos == -1:
                break
            
            mode = mode_name[:space_pos]
            name = mode_name[space_pos + 1:]
            
            # Extraire le hash (20 bytes après le null)
            hash_start = null_pos + 1
            hash_end = hash_start + 20
            
            if hash_end > len(content):
                break
            
            sha = content[hash_start:hash_end].hex()
            
            # Créer l'entrée
            entry = TreeEntry(mode=mode, name=name, sha=sha)
            entries.append(entry)
            
            pos = hash_end
        
        return cls(entries)
    
    def find_entry(self, name: str) -> Optional[TreeEntry]:
        """Trouve une entrée par son nom."""
        for entry in self.entries:
            if entry.name == name:
                return entry
        return None


class Commit(GitObject):
    """Représente un objet commit Git."""
    
    def __init__(self, tree_hash: str, message: str, author: str, parent_hash: str = None, timestamp: str = None):
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash
        self.author = author
        self.message = message
        self.timestamp = timestamp or "2024-01-01 00:00:00"
        super().__init__(b"")  # Le contenu sera calculé lors de la sérialisation
        self.type = "commit"
    
    def serialize(self) -> bytes:
        """Sérialise le commit."""
        lines = [
            f"tree {self.tree_hash}",
            f"author {self.author} {self.timestamp}",
            f"committer {self.author} {self.timestamp}",
            ""
        ]
        
        if self.parent_hash:
            lines.insert(1, f"parent {self.parent_hash}")
        
        lines.append(self.message)
        
        return '\n'.join(lines).encode('utf-8')
    
    @classmethod
    def from_hash(cls, commit_hash: str) -> 'Commit':
        """Crée un commit à partir de son hash."""
        # Lire depuis le stockage
        path = f".fyt/objects/commit/{commit_hash[:2]}/{commit_hash[2:]}"
        with open(path, 'rb') as f:
            compressed_data = f.read()
        content = zlib.decompress(compressed_data)
        
        # Parser le contenu
        lines = content.decode('utf-8').split('\n')
        
        tree_hash = None
        parent_hash = None
        author = None
        timestamp = None
        message_lines = []
        
        for line in lines:
            if line.startswith('tree '):
                tree_hash = line[5:]
            elif line.startswith('parent '):
                parent_hash = line[7:]
            elif line.startswith('author '):
                parts = line[7:].split(' ', 1)
                if len(parts) >= 2:
                    author = parts[0]
                    timestamp = parts[1]
            elif line.startswith('committer '):
                continue
            elif line == '':
                continue
            else:
                message_lines.append(line)
        
        message = '\n'.join(message_lines)
        
        return cls(tree_hash, message, author, parent_hash, timestamp)