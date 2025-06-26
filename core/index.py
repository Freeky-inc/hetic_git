# core/index.py

"""
# core/index.py
Module pour la gestion de l'index Git.
Il permet d'ajouter des fichiers à l'index, de sauvegarder et de charger l'index depuis un fichier.
"""
import json
import os

class GitIndex:
    def __init__(self, path=".git/index"):
        self.path = path
        self.entries = {}
        self.load()

    def add(self, filename, sha):
        self.entries[filename] = sha
        self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.entries, f)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.entries = json.load(f)
