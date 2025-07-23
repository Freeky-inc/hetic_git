# core/refs.py

"""
Module pour la gestion des références Git.
"""
import os
from typing import Optional


class GitRefs:
    """Gère les références Git (HEAD, branches, tags)."""
    
    def __init__(self, git_dir: str):
        self.git_dir = git_dir
        self.head_path = os.path.join(git_dir, "HEAD")
        self.refs_dir = os.path.join(git_dir, "refs")
    
    def set_head(self, ref: str, symbolic: bool = True):
        """Définit HEAD."""
        try:
            if symbolic:
                # HEAD symbolique (pointe vers une référence)
                with open(self.head_path, 'w') as f:
                    f.write(f"ref: {ref}\n")
            else:
                # HEAD détaché (pointe directement vers un commit)
                with open(self.head_path, 'w') as f:
                    f.write(f"{ref}\n")
        except Exception as e:
            print(f"Erreur lors de la définition de HEAD: {e}")
    
    def get_head(self) -> Optional[str]:
        """Récupère le hash du commit pointé par HEAD."""
        try:
            if not os.path.exists(self.head_path):
                return None
            
            with open(self.head_path, 'r') as f:
                content = f.read().strip()
            
            if content.startswith('ref: '):
                # HEAD symbolique
                ref_path = content[5:]
                ref_file = os.path.join(self.git_dir, ref_path)
                if os.path.exists(ref_file):
                    with open(ref_file, 'r') as f:
                        return f.read().strip()
                return None
            else:
                # HEAD détaché
                return content
        except Exception as e:
            print(f"Erreur lors de la lecture de HEAD: {e}")
            return None
    
    def write_ref(self, ref_name: str, commit_hash: str):
        """Écrit une référence."""
        try:
            ref_path = os.path.join(self.refs_dir, ref_name)
            os.makedirs(os.path.dirname(ref_path), exist_ok=True)
            
            with open(ref_path, 'w') as f:
                f.write(f"{commit_hash}\n")
        except Exception as e:
            print(f"Erreur lors de l'écriture de la référence {ref_name}: {e}")
    
    def read_ref(self, ref_name: str) -> Optional[str]:
        """Lit une référence."""
        try:
            ref_path = os.path.join(self.refs_dir, ref_name)
            if os.path.exists(ref_path):
                with open(ref_path, 'r') as f:
                    return f.read().strip()
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture de la référence {ref_name}: {e}")
            return None 