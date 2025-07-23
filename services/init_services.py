import os
from core import Repository

def init_repo():
    """
    Initialise un nouveau dépôt Git en utilisant le Repository du core.
    """
    repo = Repository()
    if repo.init():
        print("Dépôt initialisé.\nVous êtes dans la branche 'main'.")
    else:
        print("Erreur lors de l'initialisation du dépôt.")