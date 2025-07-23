# commands/init.py
"""
Module pour la commande 'init', qui initialise un nouveau dépôt Git.
"""
from services.init_services import init_repo

def run():
    """
    Exécute la commande init.
    """
    init_repo()