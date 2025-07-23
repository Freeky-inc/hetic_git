# commands/status.py
"""
Module pour la commande 'status', qui affiche l'état du dépôt.
"""
from services.status_services import status

def run(args):
    """
    Exécute la commande status.
    """
    status()