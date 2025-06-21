# core/objects.py

"""
Module pour la gestion des objets Git (Blob, Tree, Commit).
Ce module fournit une classe `GitObject` qui représente un objet Git générique.
Il permet de sérialiser, hacher et stocker des objets dans un dépôt Git.
"""
import hashlib, os, zlib

class GitObject:
    def __init__(self, content, type_):
        self.type = type_
        self.content = content
        self.hash = self.compute_hash()

    def serialize(self):
        return f"{self.type} {len(self.content)}\0".encode() + self.content

    def compute_hash(self):
        return hashlib.sha1(self.serialize()).hexdigest()
    
    def store(self):
        sha = self.sha1()
        path = f".git/objects/{sha[:2]}/{sha[2:]}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(zlib.compress(self.serialize()))
        return sha

    def __repr__(self):
        return f"GitObject(hash={self.hash}, content={self.content})"
    

class Blob(GitObject):
    def __init__(self, data: bytes):
        super().__init__("blob", data)

class Tree(GitObject):
    def __init__(self, entries: list):
        content = "\n".join(entries).encode()
        super().__init__(content, "tree")

class Commit(GitObject):
    def __init__(self, tree_hash: str, message: str, author: str, date: str):
        content = f"tree {tree_hash}\nmessage {message}\nauthor {author}\ndate {date}".encode()
        super().__init__(content, "commit")
        self.tree_hash = tree_hash
        self.message = message
        self.author = author
        self.date = date