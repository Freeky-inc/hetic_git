# commands/commit.py
"""
Module pour la commande 'commit', qui crée un commit avec les fichiers staged.
"""
from services.commit_services import commit

def run(message):
    """
    Exécute la commande commit.
    """
    commit(message)