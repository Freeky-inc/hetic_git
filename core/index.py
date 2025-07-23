# core/index.py

"""
Module pour la gestion de l'index Git.
"""
import os
import json
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class IndexEntry:
    """Représente une entrée dans l'index Git."""
    filename: str
    sha: str
    mode: str
    stage: int = 0


class GitIndex:
    """Gère l'index Git (staging area)."""
    
    def __init__(self, index_path: str):
        self.index_path = index_path
        self.entries: Dict[str, IndexEntry] = {}
        self.load()
    
    def load(self):
        """Charge l'index depuis le fichier."""
        try:
            if os.path.exists(self.index_path):
                with open(self.index_path, 'r') as f:
                    data = json.load(f)
                    for filename, entry_data in data.items():
                        self.entries[filename] = IndexEntry(
                            filename=entry_data.get('filename', filename),
                            sha=entry_data.get('sha', ''),
                            mode=entry_data.get('mode', '100644'),
                            stage=entry_data.get('stage', 0)
                        )
        except Exception as e:
            print(f"Erreur lors du chargement de l'index: {e}")
            self.entries = {}
    
    def save(self):
        """Sauvegarde l'index dans le fichier."""
        try:
            data = {}
            for filename, entry in self.entries.items():
                data[filename] = {
                    'filename': entry.filename,
                    'sha': entry.sha,
                    'mode': entry.mode,
                    'stage': entry.stage
                }
            
            with open(self.index_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'index: {e}")
    
    def add(self, filename: str, blob_hash: str, mode: str = "100644"):
        """Ajoute un fichier à l'index."""
        self.entries[filename] = IndexEntry(
            filename=filename,
            sha=blob_hash,
            mode=mode
        )
        self.save()
    
    def remove(self, filename: str):
        """Retire un fichier de l'index."""
        if filename in self.entries:
            del self.entries[filename]
            self.save()
    
    def get_entry(self, filename: str) -> Optional[IndexEntry]:
        """Récupère une entrée de l'index."""
        return self.entries.get(filename)
    
    def get_all_files(self) -> List[str]:
        """Récupère tous les fichiers de l'index."""
        return list(self.entries.keys())
    
    def clear(self):
        """Vide l'index."""
        self.entries.clear()
        self.save() 